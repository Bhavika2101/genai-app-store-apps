import os
import toml
from h2o_wave import main, app, Q, ui, data
from typing import Optional, List
from pathlib import Path
from loguru import logger

import asyncio
from src.gradio import get_client, upload_data, ask_query, get_sources, get_collection_id
from src.utils import format_docs_table, get_rfi_response, update_rfi, edit_rfi, heap_analytics, validate_url, download_and_read

base_path = (Path(__file__).parent / "../").resolve()
tmp_path = f"{base_path}/var/lib/tmp"
sample_q = {
    "q1" : "Could you give one success story about implementations of your AI solutions in Financial Industry?",
    "q2" : "What measures are in place to protect data in H2O Managed AI Cloud?",
    "q3" : "What is the recommend machine setup for LLM Studio?"
}

async def user_variables(q: Q):
    # settings = toml.load(f"{base_path}/src/configs/env.toml")
    try:
        q.user.model_client = await q.run(get_client, q.app.model_host, api_key=q.app.host_api)
        q.app.collection_id = await q.run(get_collection_id, q.user.model_client, q.app.langchain_mode, q.app.collection_id)
    except Exception as e:
        q.page['meta'] = ui.meta_card(box='', notification_bar=ui.notification_bar(
                text='An error occurred during loading the model client. Please try later!',
                type='error',
            ))
        logger.error(e)

async def initialize_app(q: Q):
    logger.info("Initializing the app for all users and sessions - this runs the first time someone visits this app")
    q.app.toml = toml.load("./app.toml")
    
    q.app.model_host = os.getenv("H2OGPTE_URL", "https://h2ogpte.genai.h2o.ai/")
    q.app.host_api = os.getenv("H2OGPTE_API_TOKEN", "")
    q.app.langchain_mode = os.getenv("COLLECTION_NAME", "H2O_DEMO_RFI")
    
    model_client = get_client(q.app.model_host, q.app.host_api)
    q.app.collection_id = get_collection_id(model_client, q.app.langchain_mode)
    
    q.app.loader, = await q.site.upload(['./static/loader.gif'])
    q.app.initialized = True

def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

def clear_cards(q, ignore: Optional[List[str]] = []) -> None:
    if not q.client.cards:
        return

    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)

async def set_rfi_update_cards(q:Q, clear: bool):
    if clear:
        q.page["questionnaire"].update_question_txt.value = ""
        q.page["questionnaire"].update_response_txt.value = ""

        q.page["questionnaire"].update_question_txt.visible = False
        q.page["questionnaire"].update_response_txt.visible = False
        q.page["questionnaire"].update_response.visible = False
    else:
        q.page["questionnaire"].update_question_txt.visible = True
        q.page["questionnaire"].update_response_txt.visible = True
        q.page["questionnaire"].update_response.visible = True


async def file_upload(q: Q):
    q.page["sidebar"].value = "#datasets"
    q.page["dataset"].error_bar.visible = False
    q.page["dataset"].success_bar.visible = False
    q.page["dataset"].progress_bar.visible = True

    await q.page.save()
    
    data_pdf = q.args.data_pdf
    user_url = q.args.ingest_url
    if (data_pdf is None and user_url is None) or (user_url is not None and not validate_url(user_url)):
        q.page["dataset"].error_bar.visible = True
        q.page["dataset"].progress_bar.visible = False
    else:
        usr_pdf_path = None
        if data_pdf:
            usr_pdf_path = await q.site.download(
                data_pdf[0], f"{tmp_path}/jobs"
            )

        q.page["dataset"].error_bar.visible = False
        q.user.usr_pdf = usr_pdf_path
        logger.debug(f"The user uploaded loacl path is {usr_pdf_path}")
        logger.debug(f"The user URL path is {user_url}")
            
        try:
            res = await q.run(upload_data, file=usr_pdf_path, url= user_url, model_host=q.app.model_host, host_api=q.app.host_api, collection_id=q.app.collection_id)
            if not res:
                raise ValueError('Ingestion of documents failed!')
            
            q.client.docs = await q.run(get_sources, model_host=q.app.model_host, 
                                        host_api=q.app.host_api, 
                                        langchain_mode=q.app.langchain_mode)
            q.page["dataset"].docs_table.rows = format_docs_table(q.client.docs)
            q.page["dataset"].progress_bar.visible = False
            q.page["dataset"].success_bar.visible = True
        except:
            q.page["dataset"].progress_bar.visible = False
            q.page["dataset"].error_bar.visible = True

async def create_edit_dialog(q: Q, query, resp):
    q.page['meta'].dialog = ui.dialog(
            title='Human in the loop - Review/Edit Response',
            name='edit_dialog',
            items=[
                ui.textbox(name='update_question_txt', label='Question', readonly=True, visible=True, multiline=True, value=query),
                ui.textbox(name='update_response_txt', label='Response', visible=True, multiline=True, height="200px", value=resp),
                ui.button(name="update_response", label="Update Response", visible=True, primary=True)
            ],
            closable=True,
            events=['dismissed'],
        )

async def edit_response(q: Q):
    q.client.update_idx = q.args.rfi_table[0]
    
    if q.client.rfi_responses is not None:
        query, resp = edit_rfi(q.client.rfi_responses, q.client.update_idx)
        await create_edit_dialog(q, query, resp)
    else:
        q.client.update_idx=None
        await set_rfi_update_cards(q, True)

async def update_response(q: Q):
    if q.client.rfi_responses is not None and q.client.update_idx is not None and q.args.update_response_txt:
        upd_res = q.args.update_response_txt
        _rows = update_rfi(q.client.rfi_responses, q.client.update_idx, upd_res)
        q.page["questionnaire"].rfi_table.rows = _rows
    
    q.client.update_idx = None
    q.page['meta'].dialog = None
    # await set_rfi_update_cards(q, True)
    
async def rfi_file_upload(q: Q):
    try:  
        q.page["sidebar"].value = "#questionnaire"
        q.client.update_idx = None
        q.client.rfi_responses = None
        
        await set_rfi_update_cards(q, True)
        q.page["questionnaire"].rfi_sep.visible = False
        q.page["questionnaire"].rfi_table.visible = False
        q.page["questionnaire"].error_bar.visible = False
        q.page["questionnaire"].success_bar.visible = False
        q.page["questionnaire"].progress_bar.visible = True

        await q.page.save()

        data_pdf = q.args.rfi_file if q.args.rfi_file else q.args.ingest_rfi
        usr_file_path = download_and_read(data_pdf, f"{tmp_path}/jobs")
        
        if data_pdf is None or usr_file_path is None:
            q.page["questionnaire"].error_bar.visible = True
            q.page["questionnaire"].progress_bar.visible = False
        else:
            # if data_pdf:
            #     usr_file_path = await q.site.download(
            #         data_pdf[0], f"{tmp_path}/jobs"
            #     )
            q.page["dataset"].error_bar.visible = False
            q.user.usr_file = usr_file_path
            logger.debug(f"The user uploaded local path is {usr_file_path}")
                
            rfi_cols, rfi_rows, df_rfi = await q.run(get_rfi_response,
                                                    q,
                                                    file_path=usr_file_path, 
                                                    model_host=q.app.model_host,
                                                    host_api=q.app.host_api, 
                                                    langchain_mode=q.app.langchain_mode)
            
            # Delete the file once done
            if os.path.isfile(usr_file_path):
                os.remove(usr_file_path)
            
            q.client.rfi_responses = df_rfi
            q.page["questionnaire"].rfi_table.columns = rfi_cols
            q.page["questionnaire"].rfi_table.rows = rfi_rows

            q.page["questionnaire"].progress_bar.visible = False
            q.page["questionnaire"].rfi_sep.visible = True
            q.page["questionnaire"].rfi_table.visible = True
    except Exception as e:
        logger.debug(f"Error occured: {e}")
        q.client.rfi_responses = None
        q.page["questionnaire"].progress_bar.visible = False
        q.page["questionnaire"].error_bar.visible = True

# Add RFI Datasets Upload UI
async def rfi_query_ui(q: Q):
    clear_cards(q)
    q.page["sidebar"].value = "#questionnaire"
    
    add_card(
        q,
        "questionnaire",
        ui.form_card(
            box="content",
            items=[
                ui.message_bar(
                    name="error_bar",
                    type="error",
                    text="Please input a file to URL to upload!",
                    visible=False,
                ),
                ui.message_bar(name="success_bar", type="success", text="Files Uploaded Successfully!", visible=False),
                # ui.textbox(name="table_name", label="Table Name", required=True),
                ui.file_upload(
                    name="rfi_file",
                    label="Please select a file to upload",
                    multiple=False,
                    compact=True,
                    file_extensions=["csv", "xlsx"],
                    required=True,
                    max_file_size=5000,  # Specified in MB.
                    visible = False,
                    tooltip="Please select a file to query!",
                ),
                ui.textbox(name='ingest_rfi', label='RFI Questionnaire from URL', required=True, 
                           tooltip="Please provide a URL to RFI Questionnaire. Formats supported: CSV & Excel! \
                           \n Sample URL: https://raw.githubusercontent.com/narasimhard/demo-data/main/RFIQueriesLLM.xlsx"),
                ui.progress(
                    name="progress_bar", width="100%", label="Uploading file & querying!", visible=False
                ),
                ui.button(name="rfi_file_upload", label="Submit", primary=True),
                ui.separator(name="rfi_sep",label='Below are the responses for the RFI Queries in the Document!', visible=False),
                ui.table(name='rfi_table', 
                         multiple=False, 
                         height="1", width="1", 
                         visible=False, 
                         downloadable=True,
                         columns=[
                                ui.table_column(name='index', label='Index')
                            ], rows=[]
                        ),
                ui.textbox(name='update_question_txt', label='Question', readonly=True, visible=False, multiline=True, value=""),
                ui.textbox(name='update_response_txt', label='Response', visible=False, multiline=True, height="200px", value=""),
                ui.button(name="update_response", label="Update Response", visible=False, primary=False)
            ],
        ),
    )


# Add Datasets Upload UI
async def datasets(q: Q):
    clear_cards(q)
    q.page["sidebar"].value = "#datasets"
    if q.client.docs is None:
        q.client.docs = await q.run(get_sources, model_host=q.app.model_host, 
                                    host_api=q.app.host_api, 
                                    langchain_mode= q.app.langchain_mode) 
    add_card(
        q,
        "dataset",
        ui.form_card(
            box="content",
            items=[
                ui.message_bar(
                    name="error_bar",
                    type="error",
                    text="Please input a file to URL to upload!",
                    visible=False,
                ),
                ui.message_bar(name="success_bar", type="success", text="Files Uploaded Successfully!", visible=False),
                # ui.textbox(name="table_name", label="Table Name", required=True),
                ui.file_upload(
                    name="data_pdf",
                    label="Please select a file to upload",
                    multiple=False,
                    compact=True,
                    file_extensions=["pdf", "docx"],
                    required=True,
                    max_file_size=5000,  # Specified in MB.
                    visible = False,
                    tooltip="Please select a file to upload and index!",
                ),
                ui.textbox(name='ingest_url', label='Ingest from URL', disabled=True),
                ui.progress(
                    name="progress_bar", width="100%", label="Uploading file and indexing!", visible=False
                ),
                ui.button(name="file_upload", label="Submit", primary=True, disabled=True),
                ui.separator(label=''), 
                ui.table(name='docs_table', multiple=False, height="1", width="1", columns=[
                                ui.table_column(name='index', label='Index'),
                                ui.table_column(name='document', label='Document', max_width="450px", cell_overflow='wrap'),
                                ui.table_column(name='document_type', label='Type', max_width="200px", cell_overflow='wrap'),
                                ui.table_column(name='document_status', label='Status', max_width="200px", cell_overflow='wrap'),
                            ], rows=format_docs_table(q.client.docs)
                         )
            ],
        ),
    )

# Add Chat UI
async def chat(q: Q):
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    q.page["sidebar"].value = "#chat"

    add_card(
        q,
        "queries",
        ui.form_card(
        box=ui.box('subtitle'),
        items=[
                ui.text_l("<center>Here are some examples, click to see the answer or type your own question!</center>"),
                ui.buttons(name="question", justify='around', items=[
                    ui.button(name='q1', label=sample_q["q1"], primary=False),
                    ui.button(name='q2', label=sample_q["q2"], primary=False),
                    ui.button(name='q3', label=sample_q["q3"], primary=False),
                ]),
                ui.text_l("<center>Ask away!</center>"),
            ]
        )
    )
    add_card(
        q,
        "chatbot",
        ui.chatbot_card(
            box=ui.box('content'),
            data=data('content from_user', t='list', size=-100),
            name='chatbot'
        )
    )

    q.client.cards.add("queries")
    q.client.cards.add("chatbot")

async def add_chat_cards(q:Q):
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    q.page["sidebar"].value = "#chat"

    add_card(
        q,
        "chatbot",
        ui.chatbot_card(
            box=ui.box('content'),
            data=data('content from_user', t='list'),
            name='chatbot'
        )
    )

    q.client.cards.add("chatbot")

async def user_query(q: Q, sample_query: str):
    q.page["sidebar"].value = "#chat"
    # Append user message.
    if q.args.chatbot:
        usr_q = q.args.chatbot
    elif sample_query:
        usr_q = sample_query
    
    q.page['chatbot'].data += [usr_q, True]
    # Append bot response.
    # kwargs = dict(instruction_nochat=usr_q)
    try:
        q.page['chatbot'].data += ["<center><img src={} height='40px'/></center>".format(q.app.loader), False]
        await q.page.save()

        res, ref, raw_ref = await q.run(ask_query, model_host=q.app.model_host, 
                                    host_api=q.app.host_api, 
                                    langchain_mode=q.app.langchain_mode,
                                    instruction=usr_q)
        res += ref
        q.client.last_raw_ref = raw_ref
        q.page['chatbot'].data[-1] = [res, False]
    except:
        q.page['meta'] = ui.meta_card(box='', notification_bar=ui.notification_bar(
            text='An error occurred during prediction. Please try later or a different model.',
            type='error',
        ))
        q.page['chatbot'].data[-1] = ["Sorry error occurred!", False]

async def init_ui(q: Q) -> None:
    q.page['meta'] = ui.meta_card(
        box='',
        script=heap_analytics(
            userid=q.auth.subject,
            event_properties=f"{{"
                             f"version: '{q.app.toml['App']['Version']}', "
                             f"product: '{q.app.toml['App']['Title']}'"
                             f"}}",
        ),
        layouts=[
            ui.layout(
                breakpoint="xs",
                height="100vh",
                zones=[ui.zone("device-not-supported")],
            ),
            ui.layout(name="layout_l", breakpoint='l', min_height='100vh', zones=[
                ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('sidebar', size='350px'),
                    ui.zone('body', direction=ui.ZoneDirection.COLUMN, zones=[
                        ui.zone('title', size='80px'),
                        ui.zone('subtitle', size='-1'),
                        ui.zone('content', size='1'),
                        ui.zone('footer'),
                    ]),
                ])
            ])
        ],
        title='RFI Assistant',
    )

    q.page["device-not-supported"] = ui.form_card(
        box="device-not-supported",
        items=[
            ui.text_xl(
                "This app was built for desktop; it is not available on mobile or tablets."
                )
            ]
        )

    sidebar_logo, = await q.site.upload(['./static/h2o-logo.svg'])
    q.page['sidebar'] = ui.nav_card(
        box='sidebar', color='primary', title='H2O Gen AI', subtitle="Let's conquer the world!",
        value="#chat",
        # image=sidebar_logo,
        image = "https://h2o.ai/content/experience-fragments/h2o/us/en/site/header/master/_jcr_content/root/container/header_copy/logo.coreimg.svg/1696007565253/h2o-logo.svg" ,
        items=[
            ui.nav_group('', items=[
                ui.nav_item(name="#datasets", label="Upload Sources"),
                ui.nav_item(name="#questionnaire", label="Upload RFI Questionnaire"),
                ui.nav_item(name="#chat", label="Chat")
            ]),
        ],
        secondary_items=[
            ui.text('<center>Made with H2O Wave.</center>')
        ]
    )

    q.page['chatbot'] = ui.chatbot_card(
        box=ui.box('content'),
        data=data('content from_user', t='list'),
        name='chatbot'
    )

    q.client.cards.add("chatbot")
    q.client.cards.add("queries")
    
    # header_logo, = await q.site.upload(['./static/sample.png'])
    q.page['title'] = ui.header_card(
        box='title',
        title='H2O RFI Assistant',
        color='card',
        subtitle='Powered by H2O AI',
        # image=header_logo,
    )

async def init_client(q: Q):
    q.client.cards = set()
    await init_ui(q)
    q.client.rfi_responses = None
    q.client.update_idx = None
    q.client.last_raw_ref = None
    try:
        q.client.docs = await q.run(get_sources, model_host=q.app.model_host, 
                                    host_api=q.app.host_api, 
                                    langchain_mode=q.app.langchain_mode)
    except:
        q.page['meta'] = ui.meta_card(box='', notification_bar=ui.notification_bar(
                text='An error occurred during loading the model client. Please try later!',
                type='error',
            ))
    q.client.initialized = True
    
@app('/')
async def serve(q: Q):
    if not q.app.initialized:
        await initialize_app(q)
    
    if not q.user.initialized:
        q.user.initialized = True
    
    if not q.client.initialized:
        await user_variables(q)
        await init_client(q)

    # Clear notification bar each time
    q.page['meta'].notification_bar = None

    if q.args.chatbot:
        await user_query(q, sample_query=None)
    elif q.args.rfi_table and len(q.args.rfi_table) > 0:
        await edit_response(q)
    elif q.args.update_response or q.events.edit_dialog:
        await update_response(q)
    elif q.args.file_upload:
        await file_upload(q)
    elif q.args.rfi_file_upload:
        await rfi_file_upload(q)
    elif q.args.q1 or q.args.q2 or q.args.q3:
        query = sample_q["q1"] if q.args.q1 else sample_q["q2"] if q.args.q2 else sample_q["q3"]
        await user_query(q, query)
    elif q.args['#'] and q.args['#'] == "questionnaire":
        await rfi_query_ui(q)
    elif q.args['#'] and q.args['#'] == "datasets":
        await datasets(q)
    elif q.args['#'] and q.args['#'] == "chat":
        await chat(q)
    else:
        await chat(q)

    await q.page.save()