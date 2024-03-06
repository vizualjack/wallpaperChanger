using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WallpaperChanger.Util;

namespace WallpaperChanger.Shared
{
    public class Screen
    {
        public int width { get; }
        public int height { get; }
        public WpcImage? wpcImage { get; private set; }
        bool hasChanged;
        public Screen(int width, int height) 
        {
            this.width = width;
            this.height = height;
            hasChanged = false;
            Logger.Debug(this, $"inititalized. Width: {width}; Height: {height}");
        }

        public Screen(int width, int height, WpcImage wpcImage) : this(width, height)
        {
            this.wpcImage = wpcImage;
        }

        public void SetWpcImage(WpcImage newWpcImage)
        {
            wpcImage = newWpcImage;
            wpcImage.Resize(this.width, this.height);
            hasChanged = true;
            Logger.Debug(this, $"got new image");
        }

        public bool HasChanged() { return hasChanged; }
        public void ResetHasChanged() { hasChanged = false; }
    }
}
