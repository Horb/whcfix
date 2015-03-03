ALTER TABLE posts DROP COLUMN image_file_path;
ALTER TABLE posts ADD COLUMN image_file_name NVARCHAR(250) null;
