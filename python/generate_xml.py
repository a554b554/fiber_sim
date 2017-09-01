import numpy as np

def parse_file1(filename):
    hairs=[]
    current_hair=[]
    with open(filename) as f:
        content = f.readlines()
        # content = content.split()
        # content = map(float(content))
        for data in content:
            data = data.split()
            data = list(map(float, data))
            if not len(data)==3:
                if len(current_hair) > 0:
                    hairs.append(current_hair)
                    current_hair=[]
            else:
                current_hair.append(data)
        hairs.append(current_hair)
    return hairs

def rescale_hairs(hairs):
    hairs = hairs * 4
    return hairs

def downsample_hairs(hairs, downscale):
    return hairs[:, ::downscale, :]

def write_head(f):
    f.write('<scene dim="3">\n')
    f.write('<simtype type="DiscreteElasticRods"/>\n')
    f.write('<camera dist="10" radius="2.58263" fov="40">\n')
    f.write('<rotation x="0.785" y="0" z="0" w="1"/>\n')
    f.write('<center x="0" y="0" z="0"/>\n')
    f.write('</camera>\n')
    f.write('<description text="fiber."/>\n')
    f.write('<duration time="2.0"/>\n')
    f.write('<integrator type="preconditioned-compliant-euler" maxnewton="0" criterion="1e-7"/>\n')
    f.write('<liquid epsilon="1.0" rho="0.95" sigma="20.6" H="1.0" beta="0.0" type="cylinder" theta="1.0471975512" h="0.001" viscosity="0.0" compute="bridge" cell="0.05" collisionstiffnessplanar="15000.0" drippingmiddle="0" drippingnear="0" dt="0.001" hairstep="1" swestep="1" gravityy="0.0"/>\n')
    # f.write('<liquid rho="1.0" sigma="67.0" type="cylinder" theta="1.0471975512" viscosity="7.4e-3" maxetaprop="6.0" collisionstiffness="10000.0" dampingmultiplier="0.00" radiusmultiplier="1.6" radiusmultiplierplanar="1.1" collisionstiffnessplanar="10000.0" massupdate="none" regularizershell="0.4" heightsmooth="1.0" capillaryaccel="0.0" dragradiusmultiplier="14.4" drippingmiddle="0" frictionmultiplierplanar="0.0" dt="0.003" hairstep="4" swestep="3" gravityy="0.0"/>\n')
    f.write('<fluidsim ox="-8.0" oy="-4.0" oz="-0.5" width="12.0" gx="72" gy="48" gz="8" init="none" rt="0.4" drawgrid="0">\n')
    # f.write('<boundary type="box" cx="-3.07591434664" cy="3.07591434664" cz="0.0" ex="2.0" ey="0.2" ez="0.2" rx="0.0" ry="0.0" rz="1.0" rw="-0.78539816339"/>\n')
    write_cylinder(f)
    f.write('</fluidsim>\n')


    # f.write('<StrandParameters>\n')
    # f.write('<radius value="0.0007"/>\n')
    # f.write('<youngsModulus value="1.047e10"/>\n')
    # f.write('<shearModulus value="5.4e9"/>\n')
    # f.write('<density value="1.32"/>\n')
    # f.write('<viscosity value="5e6"/>\n')
    # f.write('<baseRotation value="0.0"/>\n')
    # f.write('<accumulateWithViscous value="1"/>\n')
    # f.write('<accumulateViscousOnlyForBendingModes value="0"/>\n')
    # f.write('</StrandParameters>\n')

    f.write('<StrandParameters>\n')
    f.write('<radius value="0.005"/>\n')
    f.write('<youngsModulus value="3.4e9"/>\n')
    f.write('<shearModulus value="5.4e7"/>\n')
    f.write('<density value="1.3"/>\n')
    f.write('<viscosity value="5e7"/>\n')
    f.write('<baseRotation value="0.0"/>\n')
    f.write('<accumulateWithViscous value="1"/>\n')
    f.write('<accumulateViscousOnlyForBendingModes value="0"/>\n')
    f.write('</StrandParameters>\n')  
    return

cylinder_idx=[]

def write_cylinder(f):
    #todo
    space = 10.5
    for i in range(2):
        f.write('<boundary type="capsule" cx="0.0" cy="1.6" cz="'+str(i*space)+'" radius="0.5" halflength="10.5"/>\n')
        f.write('<boundary type="capsule" cx="0.0" cy="1.6" cz="'+str(-i*space)+'" radius="0.5" halflength="10.5"/>\n')
        f.write('<boundary type="capsule" cx="0.0" cy="-0.6" cz="'+str(i*space+space/2)+'" radius="0.5" halflength="10.5"/>\n')
        f.write('<boundary type="capsule" cx="0.0" cy="-0.6" cz="'+str(-i*space-space/2)+'" radius="0.5" halflength="10.5"/>\n')

        cylinder_idx.append(4*i)
        cylinder_idx.append(4*i+1)
        cylinder_idx.append(4*i+2)
        cylinder_idx.append(4*i+3)

    return


def write_hairs(f, hairs):
    for i in range(hairs.shape[0]):
        write_single_hair(f, hairs[i])
    return

def write_single_hair(f, hair):
    f.write('<StrandMaterialForces params="0" flow="shallow">\n')
    for i in range(hair.shape[0]):
        # if i<2 or i>hair.shape[0]-3:
        if i < 2:
            datastr = '<particle x="'+str(hair[i][0])+' '+str(hair[i][1])+' '+str(hair[i][2])+'" v="0.0 0.0 0.0" eta="0" fixed="1"/>\n'
        else:
            datastr = '<particle x="'+str(hair[i][0])+' '+str(hair[i][1])+' '+str(hair[i][2])+'" v="0.0 0.0 0.0" eta="0" fixed="0"/>\n'
        f.write(datastr)
    f.write('</StrandMaterialForces>\n\n\n')


def write_end(f):
    f.write('</scene>\n')

def write_script(f):
    for idx in cylinder_idx:
        if idx%4==0 or idx%4==1:
            f.write('<script target="solid" type="translate" x="0.0" y="-2.3" z="0" w="0.0" start="0.0" end="2.0" i="'+str(idx)+'" updatesdf="1"/>\n')
        else:
            f.write('<script target="solid" type="translate" x="0.0" y="1.3" z="0" w="0.0" start="0.0" end="1.0" i="'+str(idx)+'" updatesdf="1"/>\n')
        # <script target="solid" type="translate" x="1.0" y="0" z="0" w="0.0" start="0.0" end="1.7" i="0" updatesdf="1"/>
    return

if __name__ == '__main__':
    input_file = '../assets/rawdata/fibers.txt'
    hairs = parse_file1(input_file)
    print(len(hairs))
    nphair = np.array(hairs)
    nphair = rescale_hairs(nphair)
    nphair = downsample_hairs(nphair, downscale=50)

    output_file = '../assets/test.xml'
    f = open(output_file, 'w+')
    write_head(f)
    write_script(f)

    write_hairs(f, nphair[1:4,:,:])
    write_end(f)
