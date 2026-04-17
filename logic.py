import sqlite3
from config import dbname 
project = [(1,"Pokemons","Game with Pokemons", "https://github.com/F3lb1/tgpokemons" ,1)]
skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Telegram'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

class DB_Manager:
    def __init__(self, dbname):
        self.database = dbname
        


    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute("""CREATE TABLE  project (
                        project_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        project_name TEXT,
                        description TEXT,
                        url TEXT,
                        status_id INTEGER, 
                        FOREIGN KEY(status_id) REFERENCES status(status_id))""")
            
            con.execute("""CREATE TABLE skills( 
                        skills_id INTEGER PRIMARY KEY,
                        skills_name TEXT)""")

            con.execute("""CREATE TABLE  status (
                         status_id INTEGER PRIMARY KEY,
                         status_name TEXT
                         )""")

            con.execute("""CREATE TABLE project_skills (
                        project_id INTEGER,
                        skills_id INTEGER,
                        FOREIGN KEY(project_id) REFERENCES project(project_id),
                        FOREIGN KEY(skills_id) REFERENCES skills(skills_id)
                        )""")








            con.commit()


    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skills_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)


    def insert_project(self, data):
        sql =  " INSERT OR IGNORE INTO project (user_id,project_name,url,status_id) values(?,?,?,?)"
        self.__executemany(sql, data)



    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        project_id = self.__select_data(sql, (project_name, user_id))[0][0]
        skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))[0][0]
        data = [(project_id, skill_id)]
        sql = 'INSERT OR IGNORE INTO project_skills VALUES(?, ?)'
        self.__executemany(sql, data)


    def get_statuses(self):
        sql = "SELECT status_name FROM status"
        return self.__select_data(sql)

    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    def get_projects(self, user_id):
        sql = "SELECT* FROM project WHERE user_id = ?"
        return self.__select_data(sql, data = (user_id,))
    
    def get_project_id(self, project_name, user_id):
        return self.__select_data(sql='SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?  ', data = (project_name, user_id,))[0][0]
        
    def get_skills(self):
        return self.__select_data(sql='SELECT * FROM skills')
    
    def get_project_skills(self, project_name):
        res = self.__select_data(sql='''SELECT skills_name FROM project
JOIN project_skills ON project.project_id = project_skills.project_id 
JOIN skills ON skills.skills_id = project_skills.skills_id 
WHERE project_name = ?''', data = (project_name,) )
        return ', '.join([x[0] for x in res])
    
    def get_project_info(self, user_id, project_name):
        sql = """
SELECT project_name, description, url, status_name FROM project 
JOIN status ON
status.status_id = project.status_id
WHERE project_name=? AND user_id=?
"""
        return self.__select_data(sql=sql, data = (project_name, user_id))


    def update_projects(self, param, data):
        sql = f"UPDATE set {param} = ? WHERE project_name = ? AND user_id = ?"
        self.__executemany(sql, [data]) 
        
    def delete_project(self, user_id, project_id):
        sql = "DELETE FROM project WHERE user_id = ? AND project_id = ? "
        self.__executemany(sql, [(user_id, project_id)])
    
    def delete_skill(self, project_id, skills_id):
        sql = "DELETE FROM skills WHERE skills_id = ? AND project_id = ?  "
        self.__executemany(sql, [(skills_id, project_id)])

    def delete_status(self, status_id, status_name):
        sql = "DELETE FROM status WHERE status_id = ? AND status_name = ? "
        self.__executemany(sql, [(status_id, status_name)])

    

if __name__ == '__main__':
    manager = DB_Manager(dbname)
    #manager.create_tables()
    #manager.default_insert()
    manager.insert_project(data = project)
