GRAPH_RESPONSE_ODATA_NEXT = {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Collection(microsoft.graph.driveItem)",
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id%2cname%2clastModifiedDateTime%2cparentReference%2cfile%2cfolder%2cwebUrl%2ccontent.downloadUrl%2cshared&token=some_token",
            "value": [
                {
                    "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!573",
                    "lastModifiedDateTime": "2015-02-20T13:33:42Z",
                    "name": "Plans",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!575",
                    "lastModifiedDateTime": "2015-02-20T13:33:46Z",
                    "name": "Plans Photos",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 0,
                        "view": {}
                    }
                },
                {
                    "id": "1H9872G9875T7K1!574",
                    "lastModifiedDateTime": "2015-02-20T13:33:43Z",
                    "name": "Pland",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=tem_download_auth_token",
                    "id": "1H9872G9875T7K1!5784",
                    "lastModifiedDateTime": "2016-12-31T10:43:26Z",
                    "name": "one_note_file.onetoc2",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!574",
                        "path": "/drive/root:/Plans/Plans",
                        "siteId": "siteId"
                    },
                    "file": {
                        "mimeType": "application/octet-stream",
                        "hashes": {
                            "sha1Hash": "75955F5B9962C28DF5C8DA2344966210AF8DF586",
                            "sha256Hash": "3BC49B5CB77193EFA2E70FA02D87AC2FDE93D9522234529BEE28F97096F06CD7"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6326",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    }
                }
            ]
        }

GRAPH_RESPONSE_ODATA_LINK = {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Collection(microsoft.graph.driveItem)",
            "@odata.deltaLink": "https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id%2cname%2clastModifiedDateTime%2cparentReference%2cfile%2cfolder%2cwebUrl%2ccontent.downloadUrl%2cshared&token=token",
            "value": [
                {
                    "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    }
                }]
            }

GRAPH_RESPONSE_BATCH_25 = {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Collection(microsoft.graph.driveItem)",
            "@odata.deltaLink": "https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id%2cname%2clastModifiedDateTime%2cparentReference%2cfile%2cfolder%2cwebUrl%2ccontent.downloadUrl%2cshared&token=token",
            "value": [
                {
                    "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!573",
                    "lastModifiedDateTime": "2015-02-20T13:33:42Z",
                    "name": "Plans",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!575",
                    "lastModifiedDateTime": "2015-02-20T13:33:46Z",
                    "name": "Plans Photos",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 0,
                        "view": {}
                    }
                },
                {
                    "id": "1H9872G9875T7K1!574",
                    "lastModifiedDateTime": "2015-02-20T13:33:43Z",
                    "name": "Pland",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=tem_download_auth_token",
                    "id": "1H9872G9875T7K1!5784",
                    "lastModifiedDateTime": "2016-12-31T10:43:26Z",
                    "name": "one_note_file.onetoc2",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!574",
                        "path": "/drive/root:/Plans/Plans",
                        "siteId": "siteId"
                    },
                    "file": {
                        "mimeType": "application/octet-stream",
                        "hashes": {
                            "sha1Hash": "75955F5B9962C28DF5C8DA2344966210AF8DF586",
                            "sha256Hash": "3BC49B5CB77193EFA2E70FA02D87AC2FDE93D9522234529BEE28F97096F06CD7"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6326",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6327",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6328",
                    "lastModifiedDateTime": "2015-02-20T13:33:42Z",
                    "name": "Plans",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6329",
                    "lastModifiedDateTime": "2015-02-20T13:33:46Z",
                    "name": "Plans Photos",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 0,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6330",
                    "lastModifiedDateTime": "2015-02-20T13:33:43Z",
                    "name": "Pland",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=tem_download_auth_token",
                    "id": "1H9872G9875T7K1!6331",
                    "lastModifiedDateTime": "2016-12-31T10:43:26Z",
                    "name": "one_note_file.onetoc2",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!574",
                        "path": "/drive/root:/Plans/Plans",
                        "siteId": "siteId"
                    },
                    "file": {
                        "mimeType": "application/octet-stream",
                        "hashes": {
                            "sha1Hash": "75955F5B9962C28DF5C8DA2344966210AF8DF586",
                            "sha256Hash": "3BC49B5CB77193EFA2E70FA02D87AC2FDE93D9522234529BEE28F97096F06CD7"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6332",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6333",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6334",
                    "lastModifiedDateTime": "2015-02-20T13:33:42Z",
                    "name": "Plans",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6335",
                    "lastModifiedDateTime": "2015-02-20T13:33:46Z",
                    "name": "Plans Photos",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 0,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6336",
                    "lastModifiedDateTime": "2015-02-20T13:33:43Z",
                    "name": "Pland",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=tem_download_auth_token",
                    "id": "1H9872G9875T7K1!6337",
                    "lastModifiedDateTime": "2016-12-31T10:43:26Z",
                    "name": "one_note_file.onetoc2",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!574",
                        "path": "/drive/root:/Plans/Plans",
                        "siteId": "siteId"
                    },
                    "file": {
                        "mimeType": "application/octet-stream",
                        "hashes": {
                            "sha1Hash": "75955F5B9962C28DF5C8DA2344966210AF8DF586",
                            "sha256Hash": "3BC49B5CB77193EFA2E70FA02D87AC2FDE93D9522234529BEE28F97096F06CD7"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6338",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6339",
                    "lastModifiedDateTime": "2026-03-23T19:05:55Z",
                    "name": "root",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1"
                    },
                    "folder": {
                        "childCount": 11,
                        "view": {
                            "sortBy": "name",
                            "sortOrder": "ascending",
                            "viewType": "thumbnails"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6340",
                    "lastModifiedDateTime": "2015-02-20T13:33:42Z",
                    "name": "Plans",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6341",
                    "lastModifiedDateTime": "2015-02-20T13:33:46Z",
                    "name": "Plans Photos",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 0,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "id": "1H9872G9875T7K1!6342",
                    "lastModifiedDateTime": "2015-02-20T13:33:43Z",
                    "name": "Pland",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=AnotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!573",
                        "path": "/drive/root:/Plans",
                        "siteId": "siteId"
                    },
                    "folder": {
                        "childCount": 2,
                        "view": {}
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=tem_download_auth_token",
                    "id": "1H9872G9875T7K1!6343",
                    "lastModifiedDateTime": "2016-12-31T10:43:26Z",
                    "name": "one_note_file.onetoc2",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!574",
                        "path": "/drive/root:/Plans/Plans",
                        "siteId": "siteId"
                    },
                    "file": {
                        "mimeType": "application/octet-stream",
                        "hashes": {
                            "sha1Hash": "75955F5B9962C28DF5C8DA2344966210AF8DF586",
                            "sha256Hash": "3BC49B5CB77193EFA2E70FA02D87AC2FDE93D9522234529BEE28F97096F06CD7"
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6344",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6345",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                },
                {
                    "@microsoft.graph.downloadUrl": "https://my.microsoftpersonalcontent.com/personal/1H9872G9875T7K1/_layouts/15/download.aspx?UniqueId=uniqueId&Translate=false&tempauth=temp_download_auth_token",
                    "id": "1H9872G9875T7K1!6346",
                    "lastModifiedDateTime": "2020-03-28T20:45:43Z",
                    "name": "Document.docx",
                    "webUrl": "https://onedrive.live.com?cid=1H9872G9875T7K1&id=anotherId",
                    "parentReference": {
                        "driveType": "personal",
                        "driveId": "1H9872G9875T7K1",
                        "id": "1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876",
                        "path": "/drive/root:",
                        "siteId": ""
                    },
                    "file": {
                        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "hashes": {
                            "quickXorHash": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="
                        }
                    },
                    "shared": {
                        "scope": "users",
                        "owner": {
                            "user": {
                                "email": "johnSmith1@hotmail.com",
                                "id": "1H9872G9875T7K1",
                                "displayName": "John Katherine Smith"
                            }
                        }
                    }
                }]
            }

GRAPH_RESPONSE_2_PERMISSIONS = {
            "responses": [{
                "id": "1H9872G9875T7K1!5784",
                "body": {
                    "value": [
                        {
                            "grantedToIdentitiesV2": [
                                {
                                    "siteUser": {
                                        "email": "johnSmith1@hotmail.com"
                                    }
                                },
                                {
                                    "siteUser": {
                                        "email": "manbat@hotmail.com"
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "id": "1H9872G9875T7K1!573",
                "body": {
                    "value": [
                        {
                            "grantedToIdentitiesV2": [
                                {
                                    "siteUser": {
                                        "email": "johnSmith1@hotmail.com"
                                    }
                                },
                                {
                                    "siteUser": {
                                        "email": "manbat@hotmail.com"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }]
        }