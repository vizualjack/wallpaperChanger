using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WallpaperChanger.Shared
{
    public class Screen
    {
        public int width { get; }
        public int height { get; }
        public WpcImage wpcImage { get; private set; }
        bool hasChanged;
        public Screen(int width, int height) 
        {
            this.width = width;
            this.height = height;
            hasChanged = false;
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
        }

        public bool HasChanged() { return hasChanged; }
        public void ResetHasChanged() { hasChanged = false; }
    }
}
