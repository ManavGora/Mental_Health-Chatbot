# main.py
import asyncio
from typing import AsyncIterable, List
from decouple import config
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html, FastUI, AnyComponent
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import PageEvent, GoToEvent
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

# Create the app object
app = FastAPI()

# Message history
app.message_history: List[MessageHistoryModel] = []

# Message history model
class MessageHistoryModel(BaseModel):
    message: str = Field(title='Message')

# Chat form model
class ChatForm(BaseModel):
    chat: str = Field(title=' ', max_length=1000)

# Root endpoint
@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def api_index(chat: str | None = None, reset: bool = False) -> list[AnyComponent]:
    if reset:
        app.message_history = []
    return [
        c.PageTitle(text='FastUI Chatbot'),
        c.Page(
            components=[
                c.Heading(text='FastUI Chatbot'),
                c.Paragraph(text='This is a simple chatbot built with FastUI and MistralAI.'),
                c.Table(
                    data=app.message_history,
                    data_model=MessageHistoryModel,
                    columns=[DisplayLookup(field='message', mode=DisplayMode.markdown, table_width_percent=100)],
                    no_data_message='No messages yet.',
                ),
                c.ModelForm(model=ChatForm, submit_url=".", method='GOTO'),
                c.Link(
                    components=[c.Text(text='Reset Chat')],
                    on_click=GoToEvent(url='/?reset=true'),
                ),
                c.Div(
                    components=[
                        c.ServerLoad(
                            path=f"/api/sse/{chat}",
                            sse=True,
                            load_trigger=PageEvent(name='load'),
                            components=[],
                        )
                    ],
                    class_name='my-2 p-2 border rounded',
                ),
            ],
        ),
        c.Footer(extra_text='Made with FastUI', links=[])
    ]

# SSE endpoint for AI response
@app.get('/api/sse/{prompt}')
async def sse_ai_response(prompt: str) -> StreamingResponse:
    if not prompt or prompt == 'None':
        return StreamingResponse(empty_response(), media_type='text/event-stream')
    return StreamingResponse(ai_response_generator(prompt), media_type='text/event-stream')

# Empty response generator
async def empty_response() -> AsyncIterable[str]:
    m = FastUI(root=[c.Markdown(text='')])
    msg = f'data: {m.model_dump_json(by_alias=True, exclude_none=True)}\n\n'
    yield msg
    while True:
        yield msg
        await asyncio.sleep(10)

# AI response generator using MistralAI
async def ai_response_generator(prompt: str) -> AsyncIterable[str]:
    mistral_client = MistralClient(api_key=config('MISTRAL_API_KEY'))
    system_message = "You are a helpful chatbot. You will help people with answers to their questions."
    output = f"**User:** {prompt}\n\n"
    msg = ''

    prompt_template = "Previous messages:\n" + "\n".join([mh.message for mh in app.message_history]) + f"\nHuman: {prompt}"
    mistral_messages = [
        ChatMessage(role="system", content=system_message),
        ChatMessage(role="user", content=prompt_template)
    ]

    output += f"**Chatbot:** "
    for chunk in mistral_client.chat_stream(model="mistral-small", messages=mistral_messages):
        if token := chunk.choices[0].delta.content or "":
            output += token
            m = FastUI(root=[c.Markdown(text=output)])
            msg = f'data: {m.model_dump_json(by_alias=True, exclude_none=True)}\n\n'
            yield msg

    app.message_history.append(MessageHistoryModel(message=output))

    while True:
        yield msg
        await asyncio.sleep(10)

# Prebuilt HTML endpoint
@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI'))
