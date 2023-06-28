import requests, json, os


class CollectData():
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data = {}
        self.query  = {"archived": "false"}
        self.fetch_data()
        self.headers = {"Authorization": self.data["auth"]['token']}
    
    def fetch_data(self):
        with open(os.path.join(self.base_dir, "data.json"), "r") as file:
            self.data = json.load(file)
        return self.data

    def auth(self):
        response = requests.get("https://api.clickup.com/api/v2/team", headers=self.headers)
        print(f"Team {response.json()['teams'][0]['name']} authorized.")

    def json_pull(self):
        try:
            with open(os.path.join(self.base_dir, "data.json"), "w") as file:
                json.dump(self.data, file, indent=4)
            print('JSON updated.')
            print("\n")
        except Exception as e:
            print(e)

    def tasks_json_update(self, list_name, tasks):
        for name, id in tasks:
            self.data["lists"][list_name.lower()]["tasks"][name] = {
                'id': id,
                "subtasks": []}
        self.json_pull()

    def get_dept(self, task):
        task = task.lower()
        try:
            list_id = self.data["lists"][task]["id"]
        except KeyError:
            print("List name not found")
            return
        url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"
        tasks = requests.get(url, headers=self.headers).json()
        '''
        macro = [(tasks["tasks"][x]["name"], tasks["tasks"][x]["id"]) for x in range(0, len(tasks["tasks"]))]
        print("Found following categories:")
        for p in macro:
            print(p[0])
        self.tasks_json_update(task, macro)
        '''
        return tasks["tasks"]

    def get_subtasks(self, task):
        task_name = task.upper()
        try:
            task_id = self.data["lists"]["animation"]["tasks"][task_name]["id"]
            print(f"Category ID: {task_id}. Fetching subtasks for '{task_name}'...")
        except KeyError:
            print("Category not found")
        url = "https://api.clickup.com/api/v2/task/" + task_id + '?include_subtasks=true'
        subtasks = requests.get(url, headers=self.headers).json()['subtasks']
        self.data["lists"]["animation"]["tasks"][task_name]["subtasks"] = subtasks
        print("Found following subtasks:")
        for s in subtasks:
            print(s['name'].lower())
        self.json_pull()
        return [x['name'].lower() for x in subtasks]
