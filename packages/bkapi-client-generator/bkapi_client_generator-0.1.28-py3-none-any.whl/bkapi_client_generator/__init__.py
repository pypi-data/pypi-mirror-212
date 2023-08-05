import os
from subprocess import check_call

__base_dir__ = os.path.dirname(__file__)


class GenerateFailed(Exception):
    pass


class ExpandSwaggerError(Exception):
    pass


class GenerateMarkdownError(Exception):
    pass


def generate_client(name: str, client_package: str, swagger: str, template_name: str, output: str) -> str:
    template_dir = os.path.join(__base_dir__, f"templates/{template_name}")
    if not os.path.exists(template_dir):
        raise GenerateFailed("template does not exist")

    code = check_call(
        [
            os.path.join(__base_dir__, "bkapi-client-generator"),
            "client",
            "--template-dir",
            template_dir,
            "--output",
            output,
            "--name",
            name,
            "--client-package",
            client_package,
            "--swagger",
            swagger,
        ]
    )

    if code != 0:
        raise GenerateFailed(code)

    return os.path.join(output, name)


def expand_swagger(swagger: str, swagger_format: str, output: str):
    code = check_call(
        [
            os.path.join(__base_dir__, "swagger"),
            "expand",
            "--output",
            output,
            "--format",
            swagger_format,
            swagger,
        ]
    )

    if code != 0:
        raise ExpandSwaggerError(code)

    return output


def generate_markdown(swagger: str, language: str, output: str):
    template = os.path.join(__base_dir__, f"templates/markdown/{language}/docs.md.gotmpl")
    if not os.path.exists(template):
        raise GenerateMarkdownError(f"the markdown template of language {language} does not exist")

    if os.path.exists(output) and not os.path.isfile(output):
        raise GenerateMarkdownError("output should be a file")

    if not os.path.exists(os.path.dirname(output)):
        raise GenerateMarkdownError("the directory of output does not exist")

    code = check_call(
        [
            os.path.join(__base_dir__, "bkapi-client-generator"),
            "markdown",
            "--template",
            template,
            "--output",
            output,
            "--swagger",
            swagger,
        ]
    )

    if code != 0:
        raise GenerateMarkdownError(code)

    return output
