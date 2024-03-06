using Flurl.Http;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Policy;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Markup;
using WallpaperChanger.Util;
using static System.Net.Mime.MediaTypeNames;

namespace WallpaperChanger.LoadNew
{
    class WebLoader
    {
        private static string USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0";

        public static List<LoadResult<byte[]>> LoadBytesParallel(List<string> uris) 
        {
            var results = new List<LoadResult<byte[]>>();
            foreach (var thread in LoadUrisParallel(uris))
            {
                results.Add(new LoadResult<byte[]>(thread.uri, GetBytesFromResponse(thread.response)));
            }
            return results;
        }
        public static List<LoadResult<string>> LoadStringParallel(List<string> uris)
        {
            var results = new List<LoadResult<string>>();            
            foreach (var thread in LoadUrisParallel(uris))
            {
                results.Add(new LoadResult<string>(thread.uri, GetStringFromResponse(thread.response)));
            }
            return results;
        }

        private static List<WebLoaderThread> LoadUrisParallel(List<string> uris)
        {
            var threads = new List<WebLoaderThread>();
            foreach (var uri in uris)
            {
                var webLoader = new WebLoaderThread(uri);
                webLoader.Start();
                threads.Add(webLoader);
            }
            foreach (var thread in threads)
            {
                thread.Join();
            }
            return threads;
        }

        public class LoadResult<T>
        {
            public string uri { get; }
            public T result { get; }
            public LoadResult(string uri, T result)
            {
                this.uri = uri;
                this.result = result;
            }
        }

        class WebLoaderThread
        {
            public string uri { get; }
            public HttpResponseMessage response { get; private set; }
            Thread worker;
            public WebLoaderThread(string uri) 
            {
                this.uri = uri;
                worker = new Thread(Run);
            }

            public void Start() 
            { 
                worker.Start();
            }

            public void Join()
            {
                worker.Join();
            }

            private void Run()
            {
                response = Request(uri);
            }
        }

        public static byte[] LoadBytes(string uri)
        {
            var res = Request(uri);
            return GetBytesFromResponse(res);
        }

        private static byte[] GetBytesFromResponse(HttpResponseMessage response)
        {
            var stream = response.Content.ReadAsStream();
            var data = new byte[(int)stream.Length];
            stream.Read(data, 0, (int)stream.Length);
            return data;
        }

        public static string LoadString(string uri)
        {
            var t = uri.GetStringAsync();
            t.Wait();
            return t.Result;
        }

        private static string GetStringFromResponse(HttpResponseMessage response)
        {
            var task = response.Content.ReadAsStringAsync();
            task.Wait();
            return task.Result;
        }

        private static HttpResponseMessage Request(string uriString)
        {

            HttpClient client = new HttpClient();
            var uri = new Uri(uriString);
            var req = new HttpRequestMessage(HttpMethod.Get, uri);
            req.Headers.Add("User-Agent", USER_AGENT);
            var task = client.SendAsync(req, HttpCompletionOption.ResponseContentRead);
            task.Wait();
            return task.Result;
        }
    }
}
