#!/usr/bin/python

import sys
import json
import commands
import fuzzy


def read_input_dict():
    content = str()
    with open("/home/ubuntu/not-docker-monitor/test123.txt", "r") as f:
        content += f.read()
    return json.loads(content)


def main():
    input_data = dict()
    for key, value in read_input_dict().iteritems():
        if str(sys.argv[1]) == 'host':
            print key, value
        elif str(sys.argv[1]) == 'docker':
            for container_id, container_status in value['container_status'].iteritems():
                docker_ip_add = value['ip_addr'] + ':' + container_status['ports'].split(':')[1]
                if container_id not in input_data:
                    input_data[container_id] = []
                input_data[container_id].append([container_status['cpu'], container_status['mem_free'], docker_ip_add])
    # print("{}".format(json.dumps(input_data, indent=4, sort_keys=True)))

    for key, value in input_data.iteritems():
        element1 = int(round(value[0][0]))
        element2 = int(round(value[0][1]))
        weight = fuzzy.fuzzy_algorithm(element1, element2, 'element-1.csv', 'element-2.csv')
        get_cfg_line =  commands.getoutput("cat haproxy.cfg | grep " + value[0][2])
        changed = get_cfg_line.split("weight")[0] + 'weight ' + str(weight)  + ' maxconn -1'
        command = "sed -i 's/" + get_cfg_line + "/" + changed + "/g'" + " haproxy.cfg"
        commands.getoutput(command)
        print command
        # print key, weight, value[0][2]
    commands.getoutput("sudo haproxy -f /home/ubuntu/myFuzzy/haproxy.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)")


main()

