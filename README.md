## introduction
Crawler for Advorsity Data from github

### Notice
- This code crawls *reviewed* advorsity only
- If Selenium version < 4.0.0, use (<4.0.0)crawl_advosity_from_github.py instead
  - how to version check: 
  ```selenium.__version__```

### output
- AdvirsoryDB (dictionary type of binary text file)
  - key : ghsa
  - value : package, affectedVersion, patchedVersion
  - usage: pickle.load(./AdvirsoryDB.txt, f)
- AdvisoryDUMP(list type of text file)
  - ghsa: package:affectedVersion:patchedVersion

### solved problems
- patchedVers의 CSS 앨리먼트가 affectedVers와 중첩(포함관계)되서 patchedVers에 affectedVers가 들어가는 문제.
  > 현재로는 patchedVers 크롤링한뒤 홀수 번째만 필터링하여 사용중
  >> '22.08.30 해결: CSS Selector -> XPath 으로 변경
  >>   ``` 
  >> patchedVers = driver.find_elements(By.XPATH,'//*[@id="js-pjax-container"]/div/div[2]/div[1]/div[1]/div/div/div[3]/div') 
  >> ```

- 각 advisory페이지에 진입 -> 크롤링 -> 빠져나옴 을해서 부하가 많이 걸리는듯함.
  >
  >> 22.08.31 해결: 크롬드라이버 사용중에 크롬 사용하면 인터럽트가 되는 현상으로 확인
- 페이지 로딩때문에 sleep() 사용 중. 스레드로 더 빠르게할수 있을까?
  >
  >> 22.08.31 해결: try except 구문활용 에러발생시에만 sleep추가 부여하여 optimize
  >> ``` python
  >> try: 
  >>      advisoryInfos = crawl()
  >>  except Exception :
  >>      sleep(1)
  >>      print("[error]: do Crawl")
  >>      advisoryInfos = crawl() 
  >> ```
- selenium 4.0 버전 호환가능하도록 재작성필요
  >
  >> '22.08.30 해결: 4.0.0 버전 & 그 미만 버전으로 분화

### unsolved problems
- 현재는 패키지 당 취약버전 + 패치버전이 있는경우와 한패키지에 여러 버전이 영향 받는 경우가 구분이 안됨.
  > 어느 버전이 어떤 패키지에 해당하는지 구분이 안됨.
- 최초 전체 게시글 수를 긁어오기때문에 크롤링 도중에 새로운 게시글이 업로드 되면 리스트가 꼬이게 됨
  > 마지막 게시글을 못긁어오는 문제 + 같은 게시글을 두번 읽어오는 문제
  >>  프로그램 실행시간이 길다는 점에서 근본적인 문제가 있다.

## reference
- https://github.com/advisories?query=type%3Areviewed
- https://github.com/hyunji-Hong/Crawling_Paper
