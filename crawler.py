from __future__ import absolute_import
from tqdm import tqdm

import os
import json

from six.moves import range

import crawl_utils as cu
from automation import CommandSequence, TaskManager

NUM_BROWSERS = 10
OUTPUT_NAME = 'XXX'

# SITES = ['http://' + x for x in cu.get_top_1m(
#     os.path.expanduser('~/Desktop/%s/' % OUTPUT_NAME))]

# URL from internal/external link samples (TOP 10k/1M)
# fin = open("ALL_INTERNAL_LINKS_1mSS.json", 'r')
# data = json.loads(fin.read())
# SITES = data
# print len(SITES)
# print SITES[1000]

SITES = ["http://net.ipcalf.com"]

manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

for i in range(NUM_BROWSERS):
    browser_params[i]['cookie_instrument'] = True
    browser_params[i]['js_instrument'] = True
    # browser_params[i]['save_javascript'] = True
    browser_params[i]['save_all_content'] = True
    browser_params[i]['http_instrument'] = True
    browser_params[i]['headless'] = True

manager_params['data_directory'] = '~/Desktop/%s/' % OUTPUT_NAME
manager_params['log_directory'] = '~/Desktop/%s/' % OUTPUT_NAME

manager = TaskManager.TaskManager(manager_params, browser_params)
for site in tqdm(SITES[0:10000]):
    command_sequence = CommandSequence.CommandSequence(site, reset=True)
    command_sequence.get(sleep=10, timeout=60)
    # save the full rendered source (including all nested iframes)
    # command_sequence.recursive_dump_page_source()
    manager.execute_command_sequence(command_sequence)
manager.close()
