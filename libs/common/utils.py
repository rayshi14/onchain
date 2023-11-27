from web3 import Web3
import pandas as pd
import re
import eth_abi

def get_function_hex(function_sig): # function_sig = "balanceOf(address)"
    return Web3.keccak(text=function_sig)[:4].hex()

def get_function_param_types(function_sig): # function_sig = "balanceOf(address)"
    return function_sig[function_sig.find('(') + 1:function_sig.find(')')].split(',')

def get_log_topic(log_sig): # log_sig = "Transfer(address,address,uint256)"
    return Web3.keccak(text=log_sig).hex()

def parse_log_signature(event_text):
    event_name = re.sub(r'(?<!^)(?=[A-Z])', '_', event_text.split('(')[0])
    event_inputs = event_text[event_text.find('(') + 1:event_text.find(')')]
    topics = []
    data = []
    for event_param in event_inputs.split(','):
        event_params = event_param.strip().split(' ')
        if event_params[0].startswith('index_topic_'):
            topics.append((int(event_params[0].split('_')[-1]), tuple(event_params[1:])))
        else:
            name, t = tuple(event_params[::-1])
            name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            data.append((t, name))
            
    h = get_log_topic("{}({})".format(event_name,",".join([t[1][0] for t in topics] + [d[0] for d in data])))
    return h, event_name, topics, data

def parse_log_data(df_events, topics, data, log_name = ''):
    for i, topic in topics:
        topic_type = topic[0]
        topic_name = topic[1]
        if topic_type == 'address':
            df_events[topic_name] = '0x' + df_events['topics'].str[i].str[26:]
#             df_events.loc[df_events[topic_name] == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', topic_name] = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
        elif topic_type == 'uint256':
            df_events[topic_name] = df_events['topics'].str[i].apply(int, base=16)
        elif topic_type == 'int256':
            df_events[topic_name] = df_events['topics'].str[i].apply(int, base=16)
        else:
            df_events[topic_name] = df_events['topics'].str[i]
        
        
    data_types = [d[0] for d in data]
    data_names = [d[1] for d in data]
    
    decoded_data = df_events['data'].apply(lambda x : eth_abi.decode(data_types, bytes.fromhex(x[2:].zfill(64))))
    
    for i in range(len(data)):
        if '[' in data_types[i]:
            for j in range(decoded_data.str[i].str.len().max()):
                df_events['{}_{}'.format(data_names[i],j)] = decoded_data.str[i].str[j]
        else:
            df_events[data_names[i]] = decoded_data.str[i]

    return df_events