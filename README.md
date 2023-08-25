# Jaramgroupware Database backup tool
자람 그룹웨어의 데이터베이스 백업 툴입니다.

## 사용법
1. 해당 repository를 clone합니다.
```bash
git clone https://github.com/msng-devs/database-backup-script
```
2. **/config/config.yaml** 파일을 복사하여 원하는 경로에 저장한 후, 해당 파일을 수정합니다.
```yaml
#백업을 수행할 Database의 정보
DB_HOST:
DB_PORT:
DB_USER:
DB_PASSWORD:
DB_NAME:

# 저장된 데이터를 삭제할 날짜 (일 단위)
# ex) 7 , 이렇게 설정하면 7일이 지난 데이터는 삭제됩니다.
DATA_EXPIRED_DATE:

# 백업을 수행할 시간
# 'HH:MM:SS' or 'HH:MM' 형식
# 10:00 이면 매일 10시에 백업을 수행한다.
RUN_TIME:
```
3. Dockerfile을 빌드합니다.
```bash
docker build -t your-image-name .
```
4. Docker 컨테이너를 실행합니다.

/app/config/config.yaml 은 해당 시스템에서 사용할 설정 파일입니다.
/app/data 는 백업된 데이터 및 history 정보가 담긴 sqlite의 파일이 저장될 경로입니다.
```bash
docker run -d \
  --name your-container-name \
  -v /path/to/config.yaml:/app/config/config.yaml \
  -v /path/to/data:/app/data \
  -e TZ=your-time-zone \
  your-image-name
```