create database textsummaryDB;

use textsummaryDB;
create table tblData(
	id int AUTO_INCREMENT,
    content longtext,
    sum text,
    isTrained boolean,
    primary key (id)
);

create table tblTokenizer(
	id int AUTO_INCREMENT,
    url varchar(100),
    primary key (id)
);

create table tblSeq2Seq(
	id int AUTO_INCREMENT,
    version int,
    url varchar(100),
    f1Score float,
    createAt date,
    active boolean,
    maxTextLen int,
    maxSummaryLen int,
    embeddingDim int,
    latentDim int,
    idXTokenizer int,
    idYTokenizer int,
    primary key (id),
    foreign key (idXTokenizer) references tblTokenizer(id),
    foreign key (idYTokenizer) references tblTokenizer(id)
);

use textsummaryDB;
create table tblUser(
	id int AUTO_INCREMENT,
    username varchar(50),
    password varchar(50),
    primary key (id)
)
