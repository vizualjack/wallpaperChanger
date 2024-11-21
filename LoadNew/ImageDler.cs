using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Nodes;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using WallpaperChanger.Shared;
using WallpaperChanger.Util;

namespace WallpaperChanger.LoadNew
{
    public class ImageDler : Persistable
    {

        private static string DOMAIN = "https://wallpaperscraft.com";
        private static string WALLPAPER_CATALOG_PAGE = $"{DOMAIN}/catalog/all/";

        WpcImageContainer imageContainer;
        WpcImage.Size size;
        int page, index, lastPage;
        List<string> currentPageImageNames;
        ImageDlerGUI gui;
        public ImageDler(WpcImageContainer imageContainer, WpcImage.Size size)
        {
            this.imageContainer = imageContainer;
            this.size = size;
            page = 1;
            index = 0;
            lastPage = GetLastPage();
            currentPageImageNames = new List<string>();
            gui = new ImageDlerGUI(this, imageContainer);
        }

        public void OpenGUI()
        {
            if (gui.IsVisible) return;
            gui.Show();
        }

        public void Stop()
        {
            gui.Close();
        }

        public List<WpcImage> downloadImages(int numOfImages)
        {
            var wpcImages = new List<WpcImage>();
            var imageNames = GetNextImageNames(numOfImages);
            var links = GetLinksForImageNames(imageNames);
            foreach (var loadResult in WebLoader.LoadBytesParallel(links))
            {
                var imageNameIndex = links.IndexOf(loadResult.uri);
                var imageName = imageNames[imageNameIndex];
                var nameParts = imageName.Split('.');
                var name = nameParts[0];
                var extension = nameParts[1];
                var wpcImage = new WpcImage(WpcImage.getTypeForExtension(extension), name, extension, size, loadResult.result);
                wpcImages.Add(wpcImage);
            }
            return wpcImages;
        }

        private List<string> GetLinksForImageNames(List<string> imageNames)
        {
            var links = new List<string>();
            foreach (var imageName in imageNames)
            {
                var downloadLink = $"https://images.wallpaperscraft.com/image/single/{imageName}";
                links.Add(downloadLink);
            }
            return links;
        }

        private List<string> GetNextImageNames(int numOfImages)
        {
            var imageNames = new List<string>();
            while (imageNames.Count < numOfImages)
            {
                // make sure currentPageImageNames is filled
                while (currentPageImageNames.Count == 0)
                {
                    var pageLink = GetPageLink();
                    LoadImageNamesFromLink(pageLink);
                    if(currentPageImageNames.Count == 0) Thread.Sleep(1000);
                }
                // load image names from currentPageImageNames as long as possible
                while (true)
                {
                    var curImageName = GetNextImageName(currentPageImageNames);
                    if (curImageName == null)
                    {
                        page += 1;
                        index = 0;
                        currentPageImageNames.Clear();
                        break;
                    }
                    imageNames.Add(curImageName);
                    if (imageNames.Count >= numOfImages) break;
                }
            }
            return imageNames;
        }

        private string GetNextImageName(List<string> imageNames)
        {
            string fullImageName = null;
            while (fullImageName == null)
            {
                if (index >= imageNames.Count) return null;
                var imageName = imageNames[index];
                fullImageName = $"{imageName}_{GetImageSizeStr()}.jpg";
                index++;
            }
            return fullImageName;
        }

        private void LoadImageNamesFromLink(string searchPage)
        {
            var page = WebLoader.LoadString(searchPage);
            var imageSearch = $"/download/([^\"/]*)/{GetImageSizeStr()}";
            var matches = Regex.Matches(page, imageSearch);
            foreach (Match match in matches)
            {
                currentPageImageNames.Add(match.Groups[1].Value);
            }
        }

        private string GetPageLink()
        {
            if(page > lastPage)
            {
                page = 1;
                index = 0;
            }
            var pageLink = GetWallpaperPage();
            if (page > 1)
            {
                pageLink += $"/page{page}";
            }
            return pageLink;
        }

        private int GetLastPage()
        {
            var lastPage = -1;
            while(lastPage == -1)
            {
                var page = WebLoader.LoadString(GetWallpaperPage());
                var lastPageSearch = GetWallpaperPage().Replace(DOMAIN, "") + "/page([0-9]*)";
                var matches = Regex.Matches(page, lastPageSearch);
                foreach (Match match in matches)
                {
                    var curPage = int.Parse(match.Groups[1].Value);
                    if (curPage > lastPage) lastPage = curPage;
                }
                if(lastPage == -1) Thread.Sleep(1000);
            }
            return lastPage;
        }

        private string GetWallpaperPage()
        {
            return $"{WALLPAPER_CATALOG_PAGE}{GetImageSizeStr()}";
        }

        private string GetImageSizeStr()
        {
            return $"{size.width}x{size.height}";
        }


        const string KEY_INDEX = "index";
        const string KEY_PAGE = "page";
        public JsonNode GetSaveData()
        {
            JsonObject json = new JsonObject
            {
                { KEY_INDEX, index },
                { KEY_PAGE, page },
            };
            return json;
        }

        public void LoadFromJson(JsonNode jsonObject)
        {
            index = ((int)jsonObject[KEY_INDEX]);
            page = ((int)jsonObject[KEY_PAGE]);
        }
    }
}
