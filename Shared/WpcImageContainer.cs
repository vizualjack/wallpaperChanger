using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WallpaperChanger.Shared
{
    public class WpcImageContainer
    {
        public string? imageFolder { get; }
        public WpcImageContainer(string? imageFolder)
        {
            if (imageFolder == null) return;
            this.imageFolder = Path.GetFullPath(imageFolder);
            if (!Directory.Exists(this.imageFolder)) Directory.CreateDirectory(this.imageFolder);
        }

        public List<WpcImage> getRandomImages(int numOfImages, List<WpcImage> excludeImages) 
        {
            List<string> allImagePaths = getAllImagePaths(getExcludePaths(excludeImages));
            return getRandomImages(numOfImages, allImagePaths);
        }

        public void add(WpcImage wpcImage)
        {
            if (wpcImage.saveFolder != null && wpcImage.saveFolder != "")
                wpcImage.move(imageFolder);
            else
                wpcImage.save(imageFolder);
        }

        public void remove(WpcImage wpcImage)
        {
            if (wpcImage.saveFolder == imageFolder) File.Delete(wpcImage.getFullPath());
        }

        private List<WpcImage> getRandomImages(int numOfImages, List<string> imagePaths)
        {
            List<WpcImage> randomImages = new List<WpcImage>();
            var rnd = new Random();
            for (int i = 0; i < numOfImages; i++)
            {
                if (imagePaths.Count == 0) break;
                int pickIndex = rnd.Next(0,imagePaths.Count);
                string randomPath = imagePaths[pickIndex];
                imagePaths.RemoveAt(pickIndex);
                randomImages.Add(new WpcImage(randomPath));
            }
            return randomImages;
        }

        private List<string> getAllImagePaths(List<string> excludePaths)
        {
            List<string> allImagePaths = new List<string>();
            foreach (string path in Directory.EnumerateFiles(imageFolder))
            {
                string curPath = Path.GetFullPath(path, imageFolder);
                if (!checkIfInExcludeList(curPath, excludePaths)) allImagePaths.Add(curPath);
            }
            return allImagePaths;
        }

        private bool checkIfInExcludeList(string checkPath, List<string> excludePaths)
        {
            if (excludePaths == null || excludePaths.Count == 0) return false;
            return excludePaths.Contains(checkPath);
        }

        private List<string> getExcludePaths(List<WpcImage> wpcImages)
        {
            List<string> excludePaths = new List<string>();
            foreach (WpcImage image in wpcImages) excludePaths.Add(image.getFullPath());
            return excludePaths;
        }
    }
}
