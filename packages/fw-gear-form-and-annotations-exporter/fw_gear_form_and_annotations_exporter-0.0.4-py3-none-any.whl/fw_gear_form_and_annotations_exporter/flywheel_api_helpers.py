import logging
from functools import lru_cache

log = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def get_task(client, task_id):
    """Get task from api by task_id.

    Args:
        client (FW_Client): The Flywheel api client.
        task_id (str): The ID of the task.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/readertasks/{task_id}")


@lru_cache(maxsize=512)
def get_task_annotations(client, task_id):
    """Get task annotations from api by task_id.

    TODO: Can this be filtered by the container in which the gear is run?

    Args:
        client (FW_Client): The Flywheel api client.
        task_id (str): The ID of the task.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/readertasks/{task_id}/annotations")


@lru_cache(maxsize=512)
def get_protocol(client, protocol_id):
    """Get protocol by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol_id (str): The ID of the protocol.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/read_task_protocols/{protocol_id}")


@lru_cache(maxsize=512)
def get_form(client, form_id):
    """Get form by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        form_id (str): The ID of the form.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/forms/{form_id}")


@lru_cache(maxsize=512)
def get_project(client, project_id):
    """Get project by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        project_id (str): The ID of the project.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/projects/{project_id}")


@lru_cache(maxsize=512)
def get_subject(client, subject_id):
    """Get subject by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        subject_id (str): The ID of the subject.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/subjects/{subject_id}")


@lru_cache(maxsize=512)
def get_session(client, session_id):
    """Get session by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        session_id (str): The ID of the session.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/sessions/{session_id}")


@lru_cache(maxsize=512)
def get_acquisition(client, acquisition_id):
    """Get the acquisition by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        acquisition_id (str): The ID of the acquisition.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/acquisitions/{acquisition_id}")


@lru_cache(maxsize=512)
def get_file(client, file_id):
    """Get a file object by file_id and version

    Args:
        client (FW_Client): The Flywheel api client.
        file_id (str): The ID of the file.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/files/{file_id}")


@lru_cache(maxsize=512)
def get_files(client, parent_type, parent_id):
    """Get files by container.
    Args:
        client (FW_Client): The Flywheel api client.
        parent_type (str): Container type of the parent the gear is run within.
        parent_id (str): Container ID of the parent the gear is run within.

    Returns:
        dict: Result of the api call.
    """

    filter_string = f"{parent_type}={parent_id}"
    params = {"filter": filter_string}
    return client.get("/api/files", params=params)


@lru_cache(maxsize=512)
def get_file_annotations(client, file_id, version=None):
    """Get all annotations for a file version.

    Args:
        client (FW_Client): The Flywheel api client.
        file_id (str): The id of the file.
        version (int, optional): Version of the file. Defaults to None.

    Returns:
        dict: Result of the api call.
    """
    if version:
        filter_string = f"file_ref.file_id={file_id},file_ref.version={version}"
    else:
        filter_string = f"file_ref.file_id={file_id}"

    return client.get("/api/annotations", params={"filter": filter_string})


def get_protocol_from_name(client, protocol_name, project_id=None):
    """Get Protocol object from api by name.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol_name (str): The name of the protocol. Protocol Names are unique within
                             a project.
        project_id (str, optional): The ID of the project. Defaults to None.

    Returns:
        dict or None: The protocol object or None if not found.
    """
    filter_string = f"label={protocol_name}"
    if project_id:
        filter_string += f",project={project_id}"

    protocols = client.get("/api/read_task_protocols", params={"filter": filter_string})
    if protocols["count"] == 1:
        protocol = protocols["results"][0]
    elif protocols["count"] > 1:
        log.warning(
            "Found %s protocols with name %s.", protocols["count"], protocol_name
        )
        log.warning("Using first protocol found.")
        protocol = protocols["results"][0]
    else:
        if project_id:
            log.error(
                "No protocol found with name %s for project %s.",
                protocol_name,
                project_id,
            )
            log.error(
                "Ensure you have the protocol define for the project you are "
                "running the gear under."
            )
        else:
            log.warning("No protocol found with name %s.", protocol_name)
        protocol = None
    return protocol
