  

```conf
http {

    #http下添加这段
     map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    server{

        location / {

            #location下添加这段
	        proxy_http_version 1.1;
	        proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }


    }


}
  



	


    
```