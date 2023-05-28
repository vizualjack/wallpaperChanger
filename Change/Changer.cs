using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Design;
using System.Drawing.Drawing2D;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Forms;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using System.Windows.Xps.Packaging;
using WallpaperChanger.Shared;
using WallpaperChanger.Util;

namespace WallpaperChanger.Change
{
    public class Changer : Persistable
    {
        WpcImageContainer imageContainer;
        public List<Shared.Screen> screens { get; private set; }
        ChangerGUI gui;
        Thread guiThread;
        DateTime lastChangeTime;
        public int changeInterval;
        public Changer(WpcImageContainer imageContainer, List<Shared.Screen> screens) 
        {
            this.imageContainer = imageContainer;
            this.screens = screens;
            this.gui = new ChangerGUI(this);          
            lastChangeTime = new DateTime(0);
            changeInterval = 3600;
        }

        public void ChangeWallpaper(Shared.Screen screen)
        {
            List<WpcImage> newImages = imageContainer.getRandomImages(1, GetCurrentImages());
            if (newImages.Count > 0) screen.SetWpcImage(newImages[0]);
        }

        public void ChangeAllWallpaper()
        {
            Debug.WriteLine("ChangeAllWallpaper");
            List<WpcImage> newImages = imageContainer.getRandomImages(screens.Count, GetCurrentImages());
            foreach(var screen in screens)
            {
                if (newImages.Count <= 0) break;
                screen.SetWpcImage(newImages[0]);
                newImages.RemoveAt(0);
            }            
        }

        public void OpenGUI()
        {
            if (gui.IsVisible) return;
            gui.RefreshAllImages();
            gui.Show();
        }

        public void Stop()
        {
            gui.Close();
        }

        public void doChanges()
        {
            var nextChangeTime = lastChangeTime.AddSeconds(changeInterval);
            if(nextChangeTime.CompareTo(DateTime.Now) <= 0) ChangeAllWallpaper();
            bool wpChanged = false;
            foreach(var screen in screens)
            {
                if(screen.HasChanged()) wpChanged = true;
                screen.ResetHasChanged();
            }
            if(wpChanged)
            {
                ImagesToWallpaper();
                if(gui.IsVisible)
                {
                    gui.RefreshAllImages();
                }
                lastChangeTime = DateTime.Now;
            }
        }

        private void ImagesToWallpaper()
        {
            var mergedImage = MergeImagesHorizontal(GetCurrentImages());
            SetWallpaperImage(mergedImage);
        }

        private WpcImage? MergeImagesHorizontal(List<WpcImage> wpcImages)
        {
            var highestHeightImage = ImageUtil.getImageWithHighestHeight(wpcImages);
            if (highestHeightImage == null || highestHeightImage.size == null) return null;
            var fullImageWidth = ImageUtil.getImagesWidthSum(wpcImages);
            var fullImageHeight = highestHeightImage.size.height;
            var fullImage = new Bitmap(fullImageWidth, fullImageHeight);
            var canvas = Graphics.FromImage(fullImage);
            canvas.InterpolationMode = InterpolationMode.HighQualityBicubic;
            // Put images to canvas
            var startPos = 0;
            foreach(var wpcImage in wpcImages)
            {
                var image = wpcImage.asImage();
                if (image == null) continue;
                var bitmap = (Bitmap)image;
                bitmap.SetResolution(fullImage.HorizontalResolution, fullImage.VerticalResolution);
                canvas.DrawImage(bitmap, new Point(startPos, 0));
                startPos += bitmap.Width;
            }
            var imageData = new MemoryStream();
            canvas.Save();
            fullImage.Save(imageData, System.Drawing.Imaging.ImageFormat.Jpeg);
            return new WpcImage(WpcImage.Type.JPG, WP_NAME, "jpg", new WpcImage.Size(fullImageWidth, fullImageHeight), imageData.ToArray());
        }

        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        static extern int SystemParametersInfoW(int action, int param, string imagePath, int param1);

        const int SPI_SETDESKWALLPAPER = 20;
        const string WP_NAME = "wp";
        private void SetWallpaperImage(WpcImage image)
        {
            image.name = WP_NAME;
            Path.GetFullPath(WP_NAME);
            image.save(Path.GetPathRoot(WP_NAME));
            SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image.getFullPath(), 0);
        }

        private List<WpcImage> GetCurrentImages()
        {
            var currentImages = new List<WpcImage>();
            foreach(var screen in screens)
            {
                if (screen.wpcImage == null) continue;
                currentImages.Add(screen.wpcImage);
            }
            return currentImages;
        }

        const string KEY_CHANGEINTERVAL = "changeIntervalSecs";
        public JsonNode GetSaveData()
        {
            JsonObject json = new JsonObject
            {
                { KEY_CHANGEINTERVAL, changeInterval }
            };
            return json;
        }

        public void LoadFromJson(JsonNode jsonObject)
        {
            changeInterval = ((int)jsonObject[KEY_CHANGEINTERVAL]);
        }
    }

}
