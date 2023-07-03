wget -qO - https://www.mongodb.orgstaticpgpserver-4.4.asc  sudo apt-key add -
echo deb [ arch=amd64,arm64 ] httpsrepo.mongodb.orgaptubuntu focalmongodb-org4.4 multiverse  sudo tee etcaptsources.list.dmongodb-org-4.4.list
sudo apt-get update
sudo apt-get install mongodb-org=4.4.8 mongodb-org-server=4.4.8 mongodb-org-shell=4.4.8 mongodb-org-mongos=4.4.8 mongodb-org-tools=4.4.8
sudo mkdir -p datadb
sudo chmod 777 data
sudo chmod 777 datadb
