import data_fetcher
import data_processor
import data_drawer
import argparse

def parse_args():
    # Parse the input arguments
    parser = argparse.ArgumentParser(description='Simple tool to create mindmaps and timeline from AWS events')
    parser.add_argument('-m', '--mindmap', action='store_true', help='Print a mindmap with info regarding resources accessed')
    parser.add_argument('-t', '--timeline', action='store_true', help='Print a timeline with info regarding services used')
    parser.add_argument('-u', '--username', type=str, help='Name of the user to investigate')
    parser.add_argument('-qd', '--qradar_data', action='store_true', help='Fetch new data in QRadar')
    parser.add_argument('-fd', '--file_data', action='store_true', help='Fetch data from file')
    parser.add_argument('-if', '--input_file', type=str, help='File in which to fetch data', default='data_backup.json')
    parser.add_argument('-sd', '--store_data', action='store_true', help='Whether to store data fetched from QRadar in a file')

    return parser.parse_args()

def main():
    # Parse input arguments
    args = parse_args()

    # Check whether flags are sufficient
    input_checks(args)

    # Check where to get the data
    if args.qradar_data:
        data = data_fetcher.get_data_from_qradar(args.username, args.store_data)
        data = data['events']
    elif args.file_data:
        data = data_fetcher.get_data_from_file(args.input_file)

    # Generate Mindmap
    if args.mindmap:
        mindmap_dict = data_processor.create_mindmap_dict(data)
        data_drawer.plot_mindmap(args.username, mindmap_dict)

    # Generate timeline
    if args.timeline:
        dataframe = data_processor.create_dataframe(data)
        data_drawer.plot_timeline(args.username, dataframe)

def input_checks(args):
    # Check username
    if not args.username:
        print("Please specify a username")
        print("EXITING")
        exit()
    
    # Check output mode
    if not args.mindmap and not args.timeline:
        print("Please specify -m, -t or both")
        print("EXITING")
        exit()
    
    # Check where to fetch input data
    if args.qradar_data == args.file_data:
        print("Please specify either -qd or -fd")
        print("EXITING")
        exit() 

if __name__=="__main__":
    main()