package main

import (
	"fmt"
	"html/template"
	"net/http"
	//"github.com/nicksnyder/go-i18n/i18n"
	"github.com/BurntSushi/toml"
	"github.com/nicksnyder/go-i18n/v2/i18n"
	"golang.org/x/text/language"
	"log"
)

/*
var funcMap = map[string]interface{}{
    "T": i18n.IdentityTfunc,
}
*/

func index(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		errorHandler404(w, r, http.StatusNotFound)
		return
	}
	w.Header().Set("Content-type", "text/html")
/*
	i18n.MustLoadTranslationFile("en-us.all.json")
	T, err := i18n.Tfunc("en-US")
	fmt.Println("error - " , err)
//	temp := template.New("some_name")
	fmt.Println("error2 - " , err)


fm := template.FuncMap{
			 "T": T,
	 }
	temp, err := template.New("main").Funcs(fm).ParseFiles("template/index.html", "template/header.html", "template/footer.html")
	fmt.Println("error3 - " , err)

	temp.Execute(w, map[string]interface{}{"Title": "New cat"})

	*/
	/*
	   r.ParseForm() //анализ аргументов,
	   fmt.Println(r.Form)  // ввод информации о форме на стороне сервера
	   fmt.Println("path", r.URL.Path)
	   fmt.Println("scheme", r.URL.Scheme)
	   fmt.Println(r.Form["url_long"])
	   for k, v := range r.Form {
	       fmt.Println("key:", k)
	       fmt.Println("val:", strings.Join(v, ""))
	   }
	   fmt.Fprintf(w, "Hello Maksim!") // отправляем данные на клиентскую сторону
	*/
}

func adminka(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-type", "text/html")
	t, _ := template.ParseFiles("template/adminka/index.html", "template/header.html")
	//t.Execute(w, &page{Title: "adminka", Msg: "test2"})
	t.Execute(w, nil)

}

func errorHandler404(w http.ResponseWriter, r *http.Request, status int) {
	w.WriteHeader(status)
	if status == http.StatusNotFound {
		t, _ := template.ParseFiles("template/404.html")
		t.Execute(w, "error")
	}
}

func main() {
	bundle := &i18n.Bundle{DefaultLanguage: language.English}
	bundle.RegisterUnmarshalFunc("toml", toml.Unmarshal)
	bundle.MustLoadMessageFile("active.ru.toml")



	
	http.HandleFunc("/", index) // установим роутер
	http.HandleFunc("/adminka/", adminka)
	fs := http.FileServer(http.Dir("assets"))
	http.Handle("/assets/", http.StripPrefix("/assets/", fs))
	fmt.Println("Wallet is listening on http://localhost:9000")
	err := http.ListenAndServe(":9000", nil) // задаем слушать порт

	if err != nil {
		log.Fatal("Error: ", err)
	}
}
