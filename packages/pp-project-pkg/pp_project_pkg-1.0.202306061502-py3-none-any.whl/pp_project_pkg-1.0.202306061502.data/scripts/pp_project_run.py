## Running the pp_project.py script

import os
import argparse

def main(args,logger=None):
    logger.info('Running the pp_project pipeline')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Pp_project training Script")
    parser.add_argument("-d","--date", type=str, default='2023-06-06' , help="Date for getting the waste/production plan for. Default : 2023-06-06")
    parser.add_argument("-s","--site_id", type=int,default=30607, help="Site id. Default: 30607")
