import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pydot
import os
import data_fetcher
import config

global_logger = config.global_logger
config_object = config.config_object

# test
# Plot the timechart from a dataframe 
def plot_timeline(arn, df):
    global_logger.info('Plotting results')

    try:
        # Get colors from file to the dataset
        colors_dict = get_colors()['timechart']
        df['Color'] = df['Threat Type'].map(colors_dict)

        # Setting the layout
        plt.figure(constrained_layout=True)
        plt.title('Timeline for ' + arn)

        # Plotting the chart
        plt.barh(y=df['Service_add'], width=df['Duration'], left=df['Start'], color=df['Color'])

        # Format the x-axis labels as datetime
        date_format = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.gca().xaxis.set_tick_params(rotation=45)

        # Setting axis labels
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.locator_params(axis='x', nbins=10)

        # Exporting the chart
        plt.xlim(df['Start'].min(), df['Stop'].max())
        plt.tight_layout()  # Ensures the labels fit within the figure
        plt.savefig("out/timechart_" + arn + ".png")

    except Exception as e:
        global_logger.error('Failure in creating timechart')
        global_logger.error(str(e))

    global_logger.info('Results plotted')

# Plot a mind map
def plot_mindmap(arn, mindmap_dict):
    global_logger.info('Starting mindmap')

    try:
        # Get colors
        colors_dict = get_colors()['mindmap']

        # Define path
        # TODO when Dockerizing
        os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz\\bin'
        
        # Define graph
        #graph = pydot.Dot(graph_type="graph", rankdir="UD")
        graph = pydot.Dot(graph_type='digraph', rankdir='LR')
        root_node = pydot.Node(arn)#, label='Foo')
        graph.add_node(root_node)
        
        for resource in mindmap_dict:
            if (not resource[0]) or (resource[0] ==''):
                continue

            # Add resource node
            service = get_service_for_color(resource[1], colors_dict)
            resource_node = pydot.Node(resource[0], color=colors_dict[service])#, label='Foo')
            graph.add_node(resource_node)

            # Add edge from root to resource
            root_res_edge = pydot.Edge(arn, resource[0])
            # root_res_edge = pydot.Edge(root_node, resource_node) # not sure
            graph.add_edge(root_res_edge)

            # Add action nodes and edges
            for action in mindmap_dict[resource]:
                
                action_node = pydot.Node(action + ' - ' + str(mindmap_dict[resource][action]))
                graph.add_node(action_node)
            
                res_action_edge = pydot.Edge(resource[0], action + ' - ' + str(mindmap_dict[resource][action]))
                # res_action_edge = pydot.Edge(resource_node, action_node) # not sure
                graph.add_edge(res_action_edge)

        graph.write_dot(f"out/mindmap_{arn}.dot")
        graph.write_png(f"out/mindmap_{arn}.png")
    except Exception as e:
        global_logger.error('Failure in creating mindmap')
        global_logger.error(str(e))

    global_logger.info('Mindmap exported')

def get_colors():
    color_config_file = config_object['CONFIGFILES']['colors_file']
    return data_fetcher.get_data_from_file(f'config/{color_config_file}')

def get_service_for_color(eventsource, colors_dict_mindmap):
    eventsource_service = eventsource.split('.')[0]
    if eventsource_service in colors_dict_mindmap:
        return eventsource_service
    else:
        return 'others'