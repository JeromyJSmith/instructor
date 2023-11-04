# This file was generated by instructor
#   timestamp: 2023-09-09T20:33:42.572627
#   task_name: extract_person
#   api_path: /api/v1/extract_person
#   json_schema_path: ./input.json

from fastapi import FastAPI
from pydantic import BaseModel
from jinja2 import Template
from models import ExtractPerson

import openai
import instructor

instructor.patch()

app = FastAPI()


class TemplateVariables(BaseModel):
    biography: str


class RequestSchema(BaseModel):
    template_variables: TemplateVariables
    model: str
    temperature: int


PROMPT_TEMPLATE = Template(
    """Extract the person from the following: {{biography}}""".strip()
)


@app.post("/api/v1/extract_person", response_model=ExtractPerson)
async def extract_person(input: RequestSchema) -> ExtractPerson:
    rendered_prompt = PROMPT_TEMPLATE.render(**input.template_variables.model_dump())
    return await openai.ChatCompletion.acreate(
        model=input.model,
        temperature=input.temperature,
        response_model=ExtractPerson,
        messages=[{"role": "user", "content": rendered_prompt}],
    )  # type: ignore
