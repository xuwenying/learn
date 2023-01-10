#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>


#define PK_CLAMP(x,min,max) (x < min ? min : (x > max ? max : x))
inline uint8_t PK_CLAMP_INLINE(int x,int min,int max)
{
   return (x < min ? min : (x > max ? max : x));
} 

#include <sys/neutrino.h>
#include <sys/syspage.h>
#include <string>

// print time cost
#define TIME_START(name)                                                       \
  uint64_t start##name, end##name;          \
  start##name = ClockCycles(); \

#define TIME_END(name, info)                                                   \
  end##name = ClockCycles();                                           \
  double diff##name = (double)(end##name - start##name) /SYSPAGE_ENTRY(qtime)->cycles_per_sec * 1000;       \
  printf("%s time cost : %0.3lf ms\n", info, diff##name);

#define MAX_BUF_LEN        1024

#define FASTCV_TEST_PRINTF( FMT, ... ) \
   printf( FMT "\n", ##__VA_ARGS__ );
#define FASTCV_TEST_ERROR( FMT, ... ) \
   fprintf( stderr, FMT "\n", ##__VA_ARGS__ );


int32_t YuvResize2Rgb(uint8_t      *src, 
                  int32_t          src_width,
                  int32_t          src_height,
                  uint16_t         *resize_map,
                  uint8_t          *dst, 
                  int32_t          resize_width,
                  int32_t          resize_height)
{
   // float h_scale = src_width*1.0/resize_width;
   // float v_scale = src_height*1.0/resize_height;
   int32_t src_stride = src_width *2 ; //yuv stride
   int32_t chn = 3;
   uint32_t half = 1 << 19;

   // printf("h_scale:%f,v_scale:%f \n",h_scale,v_scale);

   // printf("src_data\n");
   // for(int ii=0; ii <10; ii++)
   // {
   //    for (size_t jj = 0; jj < 10; jj++)
   //    {
   //       int index_x = round(jj*h_scale);
   //       int index_y = round(ii*v_scale);
   //       printf("index:%d,%d,",index_x,index_y);
   //       int resize_x = resize_map[(jj*2)+ii*resize_width*2];
   //       int resize_y = resize_map[(jj*2)+1+ii*resize_width*2];
   //       printf("resize:%d,%d,",resize_x,resize_y);


   //    }
   // printf("\n");
 
   // }



   for (int32_t i = 0; i < resize_height; i++)
   {
      /* code */
      uint16_t  *p_resize_map = resize_map + i * resize_width * 2;
      uint8_t   *p_dst  = dst + (i * resize_width) * chn;
      for (int32_t j = 0; j < resize_width; j++)
      {
         /* code */
         // int index_x = resize_map[(j*2)+i*resize_width*2];
         // int index_y = resize_map[(j*2)+1+i*resize_width*2];
         int index_x = p_resize_map[(j << 1)];
         int index_y = p_resize_map[(j << 1)+1];

         int offset = index_y * src_stride + (index_x << 1);
         uint32_t index_mod = (index_x & 1) * 2;
         uint8_t *yuv_y = src + offset + 1;
         uint8_t *yuv_u = src + offset - index_mod;
         uint8_t *yuv_v = src + offset + 2 - index_mod;


         uint8_t resize_y = yuv_y[0];
         uint8_t resize_u = yuv_u[0];
         uint8_t resize_v = yuv_v[0];

         // p_dst[j * chn + 0] = (uint8_t)PK_CLAMP((yuv_y + 1.4075 * (yuv_v - 128)), 0, 255);
         // p_dst[j * chn + 1] = (uint8_t)PK_CLAMP((yuv_y - 0.3455 * (yuv_v - 128) - 0.7169 * (yuv_u - 128)), 0, 255);
         // p_dst[j * chn + 2] = (uint8_t)PK_CLAMP((yuv_y + 1.779 * (yuv_u - 128)), 0, 255);

         p_dst[j * chn + 0] = (uint8_t)PK_CLAMP((1048576 * resize_y + 1475871 * (resize_v - 128) + half) >> 20, 0, 255);
         p_dst[j * chn + 1] = (uint8_t)PK_CLAMP((1048576 * resize_y - 751724 * (resize_v - 128) - 362283 * (resize_u - 128) + half) >> 20, 0, 255);
         p_dst[j * chn + 2] = (uint8_t)PK_CLAMP((1048576 * resize_y + 1865417 * (resize_u - 128) + half) >> 20, 0, 255);

         // p_dst[j * chn + 0] = (uint8_t)PK_CLAMP_INLINE((1048576 * resize_y + 1475871 * (resize_v - 128) + half) >> 20, 0, 255);
         // p_dst[j * chn + 1] = (uint8_t)PK_CLAMP_INLINE((1048576 * resize_y - 751724 * (resize_v - 128) - 362283 * (resize_u - 128) + half) >> 20, 0, 255);
         // p_dst[j * chn + 2] = (uint8_t)PK_CLAMP_INLINE((1048576 * resize_y + 1865417 * (resize_u - 128) + half) >> 20, 0, 255);

      }
      
   }

   return 1;
   

}

int32_t  InitResizeScaler(int32_t src_width, int32_t src_height, int32_t resize_width, int32_t resize_height, uint16_t *resize_scaler)
{
   float h_scale = src_width*1.0/resize_width;
   float v_scale = src_height*1.0/resize_height;
   int32_t chn = 2;
   printf("resize_width:%d,resize_height:%d \n",resize_width,resize_height);

   printf("h_scale:%f,v_scale:%f \n",h_scale,v_scale);

   for(int ii= 0; ii < resize_height; ii++)
   {
      uint16_t   *p_dst  = resize_scaler + (ii * resize_width) * chn;
      for (int jj = 0; jj < resize_width; jj++)
      {
         int index_x = round(jj*h_scale);
         int index_y = round(ii*v_scale);
         resize_scaler[jj*chn + 0 + (ii * resize_width) * chn] = index_x;
         resize_scaler[jj*chn + 1 + (ii * resize_width) * chn] = index_y;

         // printf("%d %d ",resize_scaler[jj*chn+0],resize_scaler[jj*chn+1]);
      }
      // printf("\n第%d行:\n",ii);
     
   }
   return 1;

}



int main(int argc, char* argv[])
{
   uint64_t cpu_timer = 0;
   uint64_t qdsp_timer = 0;
 
   int32_t src_width = 1920;
   int32_t src_height = 1080;
   
   int32_t resize_width = 1408;
   int32_t resize_height = 768;

   uint8_t *pSrc_yuv = (uint8_t *)malloc(src_width * src_height * 2);

   uint8_t *pDst_rgb = (uint8_t *)malloc(resize_width * resize_height * 3);

   uint16_t *resize_scaler = (uint16_t *)malloc(resize_width * resize_height * sizeof(uint16_t) * 2);


   FILE *fp_in = fopen("./car.yuv", "rb");
   if(fp_in == NULL) 
   {
      printf("read failed\n");
      return -1;
   }

   fread(pSrc_yuv, 1, src_width * src_height * 2, fp_in);
   fclose(fp_in);

   int32_t init_ret = InitResizeScaler(src_width, src_height, resize_width, resize_height, resize_scaler);

   for (size_t i = 0; i < 100; i++)
   {
      TIME_START(t0);
      int32_t rettt = YuvResize2Rgb(pSrc_yuv, src_width, src_height, resize_scaler, pDst_rgb, resize_width, resize_height);
      TIME_END(t0,"YuvToRgb resize");
      printf("resize result:%d",rettt);
   }
   
   std::string save_name = "./vision_.rgb";
   printf("save_name:%s\n",save_name.c_str());
   // std_strlprintf( tmpFullPath, 255, "%s/%s.pgm", pTestDir, pOutputFile);

   FILE *fpOutput = fopen(save_name.c_str(), "wb" );
   if(fpOutput == NULL) 
   {
      FASTCV_TEST_PRINTF("write %s failed\n" , save_name);
      return -1;
   }

   fwrite(pDst_rgb, 1, resize_width * resize_height * 3, fpOutput);

   fclose(fpOutput);

   free(pSrc_yuv);
   free(pDst_rgb);
   free(resize_scaler);
      
   return 0;
}
