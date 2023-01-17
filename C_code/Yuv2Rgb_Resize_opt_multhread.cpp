/**=============================================================================
yuv2rgb and resize nn
mult threads

=============================================================================**/

#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>

#include <pthread.h>


#define PK_CLAMP(x,min,max) (x < min ? min : (x > max ? max : x))
inline uint8_t PK_CLAMP_INLINE(int x,int min,int max)
{
   return (x < min ? min : (x > max ? max : x));
} 


struct intput_args
{
   uint8_t  *p_src_yuv;      
   uint8_t  *p_dst;      //单通道
   uint16_t *resize_map;      //单通道
   int      src_width;
   int      src_height;
   int      resize_width;
   int      resize_height;

};


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


void* YuvResize2Rgb(void* input)
{
   // float h_scale = src_width*1.0/resize_width;
   // float v_scale = src_height*1.0/resize_height;
   struct intput_args *input_arg = (struct intput_args*) input;
   int32_t   src_width = input_arg->src_width;
   int32_t   src_height = input_arg->src_height;
   uint16_t  *resize_map = input_arg->resize_map;
   int32_t   resize_width = input_arg->resize_width;
   int32_t   resize_height = input_arg->resize_height;
   uint8_t   *src = input_arg->p_src_yuv;
   uint8_t   *dst = input_arg->p_dst;

   int32_t src_stride = src_width *2 ; //yuv stride
   int32_t chn = 3;
   uint32_t half = 1 << 19;

   // printf("YuvResize2Rgb : src_width:%d, src_height:%d\n",src_width, src_height);
   // printf("YuvResize2Rgb : src:%d,:%d\n",src[0], src[1]);

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
   pthread_exit(NULL);

}

int32_t  InitResizeScaler(int32_t src_width, int32_t src_height, int32_t resize_width, int32_t resize_height, uint16_t *resize_scaler)
{
   float h_scale = src_width*1.0/resize_width;
   float v_scale = src_height*1.0/resize_height;
   int32_t chn = 2;
   printf("resize_width:%d,resize_height:%d \n", resize_width, resize_height);

   printf("h_scale:%f,v_scale:%f \n", h_scale, v_scale);

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
   printf("init scaler successful\n");

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

   uint8_t *pSrc_yuv_batch1 = (uint8_t *)malloc(src_width * src_height * 2);
   uint8_t *pSrc_yuv_batch2 = (uint8_t *)malloc(src_width * src_height * 2);

   uint8_t *pDst_rgb_batch1 = (uint8_t *)malloc(resize_width * resize_height * 3);
   uint8_t *pDst_rgb_batch2 = (uint8_t *)malloc(resize_width * resize_height * 3);


   uint16_t *resize_scaler1 = (uint16_t *)malloc(resize_width * resize_height * sizeof(uint16_t) * 2);
   uint16_t *resize_scaler2 = (uint16_t *)malloc(resize_width * resize_height * sizeof(uint16_t) * 2);

   FILE *fp_in = fopen("./car.yuv", "rb");
   if(fp_in == NULL) 
   {
      printf("read failed\n");
      return -1;
   }
   FILE *fp_in1 = fopen("./0.yuv", "rb");
   if(fp_in1 == NULL) 
   {
      printf("read failed\n");
      return -1;
   }

   fread(pSrc_yuv_batch1, 1, src_width * src_height * 2, fp_in);
   fread(pSrc_yuv_batch2, 1, src_width * src_height * 2, fp_in1);
   printf("file read : bs1 src:%d,%d\n",pSrc_yuv_batch1[0], pSrc_yuv_batch1[1]);
   printf("file read : bs2 src:%d,%d\n",pSrc_yuv_batch2[0], pSrc_yuv_batch2[1]);


   fclose(fp_in);

   int32_t init_ret1 = InitResizeScaler(src_width, src_height, resize_width, resize_height, resize_scaler1);
   int32_t init_ret2 = InitResizeScaler(src_width, src_height, resize_width, resize_height, resize_scaler2);

   if (init_ret1 == 1 && init_ret2 == 1)
   {
      printf("init successful!!!");
   }

   printf("xxxxxxxxxxxxxxxxxxxxxx successful!!!\n");
   pthread_t threads[2];
   void* status;
   struct intput_args in_arg[2];
   for (int i=0;i<2;i++){
         in_arg[i].src_width = src_width;
         in_arg[i].src_height = src_height;
         in_arg[i].resize_height = resize_height;
         in_arg[i].resize_width = resize_width;

 
      }
   in_arg[0].resize_map = resize_scaler1;
   in_arg[1].resize_map = resize_scaler2;

   in_arg[0].p_src_yuv = pSrc_yuv_batch1;
   in_arg[1].p_src_yuv = pSrc_yuv_batch2;

   in_arg[0].p_dst = pDst_rgb_batch1;
   in_arg[1].p_dst = pDst_rgb_batch2;
   printf("src_width:%d,src_height:%d\n",in_arg[1].src_width,in_arg[1].src_height);
   // printf("xxxxxxxxxxxxxxxxxxxxxx src_width:%d,src_height:%d\n",in_arg[0].src_width,in_arg[0].src_height);

   for (size_t i = 0; i < 10; i++)
   {
      TIME_START(t0);
      //创建线程 输入 赋值
      int pthread_create_status1 = pthread_create(&threads[0],NULL,YuvResize2Rgb,(void*)&in_arg[0]);
      if(pthread_create_status1){
         printf("create thread1 fail!");
      }
      int pthread_create_status2 = pthread_create(&threads[1],NULL,YuvResize2Rgb,(void*)&in_arg[1]);
      if(pthread_create_status2){
         printf("create thread2 fail!");
      }
      pthread_join(threads[0],&status);
      pthread_join(threads[1],&status);

      TIME_END(t0,"YuvToRgb resize");
   }

   std::string save_name1 = "./0.rgb";
   printf("save_name:%s\n",save_name1.c_str());
   FILE *fpOutput1 = fopen(save_name1.c_str(), "wb" );
   if(fpOutput1 == NULL) 
   {
      FASTCV_TEST_PRINTF("write %s failed\n" , save_name1);
      return -1;
   }
   fwrite(pDst_rgb_batch1, 1, resize_width * resize_height * 3, fpOutput1);


   std::string save_name2 = "./1.rgb";
   printf("save_name:%s\n",save_name2.c_str());
   FILE *fpOutput2 = fopen(save_name2.c_str(), "wb" );
   if(fpOutput2 == NULL) 
   {
      FASTCV_TEST_PRINTF("write %s failed\n" , save_name2);
      return -1;
   }
   fwrite(pDst_rgb_batch2, 1, resize_width * resize_height * 3, fpOutput2);
  
   fclose(fpOutput1);
   fclose(fpOutput2);

   free(pSrc_yuv_batch1);
   free(pSrc_yuv_batch2);
   free(pDst_rgb_batch1);
   free(pDst_rgb_batch2);

   free(resize_scaler1);
   free(resize_scaler2);

   return 0;
}
