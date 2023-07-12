import paramiko
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_total_documents(worker):
    client = MongoClient(worker, username="admin", password="admin")
    db = client["spotify"]
    collection = db["Spotifyv3"]
    total_documents = int(collection.count_documents({}))
    
    return total_documents
    
    
def create_replication_partition(worker, partition, total_partition):
    total_documents = get_total_documents(worker)
    partition_size = total_documents // total_partition
    
    start_index = int(partition * partition_size)
    end_index = start_index + partition_size 
    
    if partition == total_partition - 1:
        extra_doc = total_documents % total_partition
        end_index += extra_doc
        
    return start_index, end_index
    
def execute_script(hostname, inicio, fim):
    print(inicio, fim)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conexão SSH
    ssh.connect(hostname, username='vlemos', password='deidarasa1')

    command = f'python3 /home/vlemos/script/request.py --inicio {inicio} --fim {fim} --genre 1'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    ssh.close()

    return output, error

if __name__ == '__main__':
   
    hostnames = ['config-server', 'worker-sl1', 'worker-sl2']
    intervalos = []
	
    for index_host in range(0, len(hostnames)):
        x, y = create_replication_partition("router", index_host, len(hostnames))
        #print(x, y)
        intervalos.append((x, y))
        
    with ThreadPoolExecutor() as executor:
        results = {}
        futures = {executor.submit(execute_script, hostname, inicio, fim): (hostname, inicio, fim)
                   for (hostname, (inicio, fim)) in zip(hostnames, intervalos)}

        for future in as_completed(futures):
            hostname, inicio, fim = futures[future]

            try:
                output, error = future.result()
                results[hostname] = {'output': output, 'error': error}
            except Exception as e:
                results[hostname] = {'output': None, 'error': str(e)}
    
    for hostname, result in results.items():
        file_ = open(f"{hostname}.json", "wt")
        print(f"--- Resultados para {hostname} ---")
        if result['output'] is not None:
            file_.write(result["output"])
            #print(result['output'])
        if result['error'] != '':
            print(f"Erro: {result['error']}")
        print()

