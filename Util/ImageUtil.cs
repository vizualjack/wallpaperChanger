using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WallpaperChanger.Shared;

namespace WallpaperChanger.Util
{
    static class ImageUtil
    {
        public static WpcImage? getImageWithHighestHeight(List<WpcImage> wpcImages)
        {
            WpcImage? highestHeightImage = null;
            foreach (var wpcImage in wpcImages)
            {
                if (highestHeightImage == null || wpcImage.size.height > highestHeightImage.size.height)
                    highestHeightImage = wpcImage;
            }
            return highestHeightImage;
        }

        public static WpcImage? getImageWithHighestWidth(List<WpcImage> wpcImages)
        {
            WpcImage? highestWidthImage = null;
            foreach (var wpcImage in wpcImages)
            {
                if (highestWidthImage == null || wpcImage.size.width > highestWidthImage.size.width)
                    highestWidthImage = wpcImage;
            }
            return highestWidthImage;
        }

        public static int getImagesWidthSum(List<WpcImage> wpcImages)
        {
            int widthSum = 0;
            foreach (var wpcImage in wpcImages)
                widthSum += wpcImage.size.width;
            return widthSum;
        }

        public static bool checkIfImageAlreadyExist(WpcImage checkImage, List<WpcImage> wpcImages)
        {
            foreach (var wpcImage in wpcImages)
            {
                if (checkImage.getFullName().Equals(wpcImage.getFullName())) 
                    return true;
            }
            return false;
        }
    }
}
