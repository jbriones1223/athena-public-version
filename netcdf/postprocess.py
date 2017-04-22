#! /usr/bin/env python2.7
import subprocess, glob, os
from netCDF4 import Dataset

#folder      = '/home/chengli/athena-public-version/3d-hs94/'
#problem     = 'hs94'
#nrb1, nrb2, nrb3 = 1, 2, 4
#bx1, bx2, bx3    = 32, 16, 16

#folder      = '/home/chengli/athena-public-version/3d-rt/'
#problem     = 'rt'
#nrb1, nrb2, nrb3 = 2, 2, 2
#bx1, bx2, bx3    = 32, 32, 32

#folder      = '/home/chengli/athena-public-version/2d-sw/'
#problem     = 'sw'
#nrb1, nrb2, nrb3 = 4, 2, 1
#bx1, bx2, bx3    = 64, 64, 1

#folder      = '/home/chengli/athena-public-version/2d-galewsky04/'
#problem     = 'galewsky04'
#nrb1, nrb2, nrb3 = 4, 4, 1
#bx1, bx2, bx3    = 128, 64, 1

#folder      = '/home/chengli/athena-public-version/2d-showman06/'
#problem     = 'showman06'
#nrb1, nrb2, nrb3 = 4, 4, 1
#bx1, bx2, bx3    = 64, 32, 1

#folder      = '/home/chengli/athena-public-version/2d-jupole/'
#problem     = 'jupole'
#nrb1, nrb2, nrb3 = 4, 4, 1
#bx1, bx2, bx3    = 128, 128, 1

#folder      = '/home/cli/athena-public-version/2d-swgv/'
#problem     = 'swgv'
#nrb1, nrb2, nrb3 = 8, 4, 1
#bx1, bx2, bx3    = 100, 50, 1

folder      = '/home/cli/athena-public-version/2d-jupiter/'
problem     = 'jupole'
nrb1, nrb2, nrb3 = 4, 4, 1
bx1, bx2, bx3    = 256, 256, 1

num_blocks  = nrb1 * nrb2 * nrb3

for i in range(num_blocks):
  print 'processing block %d ...' % i
  files = '%s/%s.block%d.*.*.nc' % (folder, problem, i)
  target = '%s.nc.%04d' % (problem, i)
  subprocess.call('ncrcat -h %s %s' % (files, target), shell = True)
  subprocess.call('ncatted -O -a %s,%s,%c,%c,%d %s' 
      % ('NumFilesInSet', 'global', 'c', 'i', num_blocks, target),
      shell = True)

  data = Dataset(target, 'a')
  loc = data.logical_location

  data.variables['x1'].setncattr('domain_decomposition', 
      [1, bx1 * nrb1, bx1 * loc[0] + 1, bx1 * (loc[0] + 1)])
  data.variables['x1b'].setncattr('domain_decomposition', 
      [0, bx1 * nrb1, bx1 * loc[0], bx1 * (loc[0] + 1)])

  data.variables['x2'].setncattr('domain_decomposition',
      [1, bx2 * nrb2, bx2 * loc[1] + 1, bx2 * (loc[1] + 1)])
  data.variables['x2b'].setncattr('domain_decomposition',
      [0, bx2 * nrb2, bx2 * loc[1], bx2 * (loc[1] + 1)])

  data.variables['x3'].setncattr('domain_decomposition',
      [1, bx3 * nrb3, bx3 * loc[2] + 1, bx3 * (loc[2] + 1)])
  #data.variables['x3b'].setncattr('domain_decomposition',
  #    [0, bx3 * nrb3, bx3 * loc[2], bx3 * (loc[2] + 1)])

  data.close()

subprocess.call('gcc -O -o mppnccombine mppnccombine.c -lnetcdf', shell = True)
subprocess.call('./mppnccombine %s.nc' % problem, shell = True)

for f in glob.glob('*.nc.????'):
  os.remove(f)


'''
for b in $(seq 0 15);
do
  echo "processing block $b ..."
  printf -v bb "%04d" $b
  ncrcat -h $folder/rt.block$b.*.*.nc rt.nc.$bb
  ncatted -O -a NumFilesInSet,global,c,i,16 rt.nc.$bb
  #files=`ls $folder/rt.block$b.out2.*.nc`;
  #echo $files
  #ext=${file##*.}
  #echo $ext
done
'''
