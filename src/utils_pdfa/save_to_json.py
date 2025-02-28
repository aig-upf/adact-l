import json

def save_json(RDP, path):
    #save nodes
    nodes=[]
    for s in RDP.states:
        if s.parent==None:
            parent = "None"
        else:
            parent= s.parent.name
        nodes.append({
             "id" : s.name,
             "source" : parent,
             "ix": str(list(s.ix))

         } )
    #save paths
    edges=[]
    for transition in RDP.transitions:
        edges.append({
            "id": transition[0]+"_"+transition[3],
            "source": transition[0],
            "target": transition[3],
            "name": transition[1]+"_"+transition[2],
            "appearances": ""

        })
    jsonfile = {"nodes": nodes, "paths": edges}
    #print(json.dumps(jsonfile, indent=4))
    save_path = './json/'+ path[1]+"_"+path[2]+"_"+path[3]+'.json'
    json.dump(jsonfile, open(save_path, 'w'), sort_keys=True, indent='\t', separators=(',', ': '))
    print("RDP saved at: ", save_path)

