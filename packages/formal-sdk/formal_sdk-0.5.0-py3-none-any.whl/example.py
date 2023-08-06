import os
from formal_sdk import client
from formal_sdk.datastore import NativeRole

apiKey = ""
c = client.Client(apiKey)
# nativerole = c.DataStoreClient.CreateNativeRole(dataStoreId="e092e9f7-bb67-4eb6-949d-a4377899b18f", nativeRoleId="tg",
#                                        nativeRoleSecret="tgga", useAsDefault=True)
#
# print(nativerole.nativeRoleId)
nativerole = c.DataStoreClient.GetNativeRole(dataStoreId="e092e9f7-bb67-4eb6-949d-a4377899b18f", nativeRoleId="tg")
print(nativerole.to_dict())

print(f'DataStoreId: {nativerole.dataStoreId}')
print(f'NativeRoleId: {nativerole.nativeRoleId}')
print(f'NativeRoleSecret: {nativerole.nativeRoleSecret}')
print(f'UseAsDefault: {nativerole.useAsDefault}')