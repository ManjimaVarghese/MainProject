from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient,__version__

connectionstring="DefaultEndpointsProtocol=https;AccountName=sample123lik;AccountKey=jLw4XvM5sS7SWou3mVBqWOYyCSrrcHin4AqXWkScaLAAC+lu/Dh/i623g0l566udVavZ0sRSndtk+AStx9AUmA==;EndpointSuffix=core.windows.net"

import uuid

blob_service_client=BlobServiceClient.from_connection_string(connectionstring)

containername=str(uuid.uuid4())

# container_client=blob_service_client.create_container(containername)

blob_client=blob_service_client.get_container_client(container="sample")

with open("aaanew.sql","wb") as h:
    k=blob_client.download_blob ("a.sql").readall()
    h.write(k)

    print(k)

