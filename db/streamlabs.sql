use streamlabs;

drop table user_subscription;
drop table user_account;

create table user_account (
	user_id varchar(64) NOT NULL,
    public_id int NOT NULL UNIQUE AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    email varchar(70) NOT NULL,
    password_hash varchar(100) NOT NULL,
    is_verified bit(1) DEFAULT 0,
    primary key (user_id)
);

create table user_subscription (
	subscription_id varchar(64) NOT NULL,
    user_id varchar(64) NOT NULL,
    created_at datetime NOT NULL,
    price decimal(7,2) NOT NULL,
    subscription_status varchar(70) NOT NULL,
    updated_at datetime NOT NULL,
    primary key (subscription_id),
    foreign key (user_id) references user_account(user_id)
);