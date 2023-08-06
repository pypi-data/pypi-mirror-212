# eco_ask

.env檔請填入以下資訊, 並放置於你終端機的工作目錄
```
LINE_CHANNEL_TOKEN=
LINE_CHANNEL_SECRET=
OPENAI_KEY=
GOOGLE_API_KEY=
IMGUR_ID=
```
使用pip安裝
```
pip install enviRobot-scoop
```
使用scoop-handler
```
from enviRobot_scoop import enviRobot_scoop
enviRobot_scoop.handle_enviRobot(dic_params, question, websocket)
```