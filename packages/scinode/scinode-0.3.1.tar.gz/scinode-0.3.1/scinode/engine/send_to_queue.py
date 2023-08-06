from scinode.utils.db import push_message
from scinode.profile.profile import profile_datas
from scinode.engine.config import broker_queue_name

# load celery tasks
if profile_datas["celery"]:
    from scinode.engine.celery import tasks


def send_message_to_queue(queue, msg):
    """Send message to the queue."""
    if profile_datas["celery"]:
        tasks.scheduler_process_message.apply_async(queue=queue, args=(msg,))
    else:
        push_message(queue, msg)


def launch_nodetree(queue, nodetree_uuid):
    """Launch nodetree"""
    msg = f"{nodetree_uuid},nodetree,action:LAUNCH"
    if profile_datas["celery"]:
        tasks.scheduler_process_message.apply_async(
            queue=broker_queue_name, args=(msg,)
        )
    else:
        push_message(broker_queue_name, msg)


def reset_nodetree(queue, nodetree_uuid):
    """Reset nodetree"""
    msg = f"{nodetree_uuid},nodetree,action:RESET"
    if profile_datas["celery"]:
        tasks.scheduler_process_message.apply_async(
            queue=broker_queue_name, args=(msg,)
        )
    else:
        push_message(broker_queue_name, msg)


def launch_node(queue, nodetree_uuid, node_name):
    """Launch node"""
    if profile_datas["celery"]:
        tasks.launch_node.apply_async(queue=queue, args=(nodetree_uuid, node_name))
    else:
        push_message(queue, f"{nodetree_uuid},node,{node_name}:action:LAUNCH")


def expose_outputs(queue, nodetree_uuid, node_name):
    """Expose outputs for the node group"""
    if profile_datas["celery"]:
        tasks.expose_outputs.apply_async(queue=queue, args=(nodetree_uuid, node_name))
    else:
        push_message(queue, f"{nodetree_uuid},node,{node_name}:action:EXPOSE_OUTPUTS")
