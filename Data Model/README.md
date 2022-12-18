# Модель данных
## База данных содержит информацию о репозиториях, коммитах, пуллреквестах и Issue. Ниже приведен список полей.
### User
- UserName
- Password
- Token
- Repos

### Repo
- Name
- Issues
- Commits
- Pull_Requests

### Commit
- Id
- Author_Name
- Author_login
- Author_email
- Data_and_time
- Changed_files

### Pull_Request
- Id
- Title
- State
- Commit_info
- Creator_name
- Creation_date
- Creator_login
- Creator_email
- Changed_files
- Comment_body
- Comment_created_date
- Comment_author_name
- Comment_author_login
- Comment_author_email
- Merger_name
- Merger_login
- Merger_email

### Issue
- Id
- Number
- Title
- State
- Task
- Creation_date
- Creator_name
- Creator_login
- Creator_email
- Changed_files
- Comment_date
- Comment_body
- Comment_author_name
- Comment_author_login
- Comment_author_email


## Оценка удельного объема информации, хранимой в модели
Пусть в базе данных N1 пользователей N2 репозиториев N3 пулреквестов  N4 коммитов и N5 Issue .
Максимальные размеры полей документа:
UserName:128 bytes
Password: 128 bytes
Token: 93 bytes
Repos: 760 bytes


Name: 256bytes
Issues: 760
Commits:760
Pull_Requests:760


Id:8 bytes
Author_Name:128 bytes
Author_login:128 bytes
Author_email:128 bytes
Data_and_time:20 bytes
Changed_files:760bytes

Id:8 bytes
Title:256 bytes
State: 100 bytes
Commit_info: 100bytes
Creator_name: 128 bytes
Creation_date:20 bytes
Creator_login: 128 bytes
Creator_email: 128 bytes
Changed_files:760bytes
Comment_body:1000 bytes
Comment_created_date:20 bytes
Comment_author_name:128 bytes
Comment_author_login:128 bytes
Comment_author_email:128 bytes
Merger_name:128 bytes
Merger_login:128 bytes
Merger_email:128 bytes

Id:8 bytes
Number:8 bytes
Title:256 bytes
State:100 bytes
Task: 1000 bytes
Creation_date:20 bytes
Creator_name:128 bytes
Creator_login:128 bytes
Creator_email:128 bytes
Changed_files:760 bytes
Comment_date:20 bytes
Comment_body:1000 bytes
Comment_author_name:128 bytes
Comment_author_login:128 bytes
Comment_author_email:128 bytes


Тогда у нас будет N1(1109)+N2(2536)+N3(3932)+N4(1172)+N5(3416) bytes максимальной объём базы
## Избыточность модели
Модель не содержит дополнительных данных, помимо исходных, а значит не является избыточной.

## Направление роста модели при увеличении количества объектов каждой сущности
Размер базы данных растет линейно по каждому параметру.

## Запросы к модели, с помощью которых реализуются сценарии использования
### Добавление
collection.new_commit({
   "Id":1,
   "Author_Name":"Pavel",
   "Author_login":"cirilohysP",
   "Author_email":"realmathsmc@gmail.com",
   "Data_and_time":"2022-12-12 19:58:48",
   "Changed_files":",Новая папка (2)/README.md"
})

### Удаление
collection.delete_commit('id' : '1')

### Обновление
collection.update_commit({"_id" : "1"}, {"$set" : {"Author_Name" :"Pavel Kravchenko"}})

### Поиск по полю
collection.find_commit({"Author_login" : "Dunkel"})


### Сортировка
collection.find().sort("Author_Name")

### Поиск по нескольким полям
collection.find_commit({"Author_Name":"Pavel", "Changed_files":",Новая папка (2)/README.md"})

![ModelData](ModelData.png)
