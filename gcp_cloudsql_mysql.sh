
###################################################################################################
#
#   Cloud SQL (MySQL)
#
#   Google Cloud Platform (GCP)
#
#   References:
#   https://cloud.google.com/sql/docs/mysql/create-instance
#   https://cloud.google.com/sql/docs/mysql/instance-settings
#   https://cloud.google.com/sdk/gcloud/reference/sql/
#
###################################################################################################


# Lists Cloud SQL instances
gcloud sql instances list


# Create Cloud SQL (MySQL) Instance
# https://cloud.google.com/sql/docs/mysql/create-instance
gcloud sql instances create z-mysql-1 \
    --database-version=MYSQL_5_7 \
    --tier=db-n1-standard-1 \
    --region=us-east1


# Set the password for the "root@%" MySQL user:
gcloud sql users set-password root % --instance z-mysql-1 --password mysql_123


# Connect to Cloud SQL (MySQL) Instance
gcloud sql connect z-mysql-1 --user=root


# Create MySQL Database
gcloud sql databases create zdatabase --instance=z-mysql-1


# List MySQL Databases
gcloud sql databases list --instance=z-mysql-1


# Delete Cloud SQL Instance
gcloud sql instances delete z-mysql-1



'''
create database zdatabase;


use zdatabase;


CREATE TABLE banking (
  transaction_id INT NOT NULL,
  customer_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  state CHAR(2),
  transaction FLOAT,
  calls INT,
  at_risk INT,
  PRIMARY KEY (transaction_id)
);


INSERT INTO banking 
    (transaction_id, customer_id, name, state, transaction, calls, at_risk) 
VALUES 
    (100001, 1001, "Danny", "NC", 100.00, 0, 0),
    (100002, 1002, "Rusty", "NV", 200.00, 1, 1),
    (100003, 1003, "Linus", "IL", 300.00, 2, 0),
    (100004, 1004, "Terry", "NV", 400.00, 3, 1),
    (100005, 1005, "Tess",  "NV", 500.00, 4, 0),
    (100006, 1001, "Danny", "NC", 200.00, 0, 0),
    (100007, 1001, "Danny", "NC", 300.00, 0, 0),
    (100008, 1002, "Rusty", "NV", 400.00, 3, 1)    
    ;


select * from banking;


select customer_id, count(*) as number_of_transactions, avg(transaction) as avg_transaction 
from banking 
group by customer_id;

'''


#ZEND
