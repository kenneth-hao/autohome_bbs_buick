DROP TABLE IF EXISTS autohome_bbs_content;
CREATE TABLE autohome_bbs_content (
  id int(20) PRIMARY KEY,
  title char(100),
  author char(50),
  content TEXT
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

