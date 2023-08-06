"""
SciNode is a platform to create node-based workflows with each node
performing a dedicated task.
"""
from scinode.nodetree import NodeTree
from scinode.utils import load_nodetree, load_node

import logging

# Define a logger object with a name 'scinode_logger'
logger = logging.getLogger("scinode_logger")
# Configure the logger object with a logging level
logger.setLevel(logging.DEBUG)
