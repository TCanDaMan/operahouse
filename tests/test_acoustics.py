import sys, math, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import acoustics as a
class AcousticsTests(unittest.TestCase):
    def test_image_source(self):
        wall=a.Plane('wall','W',(0,0,0),(1,0,0),'plaster',lambda p:True)
        source=(2,1,0); eye=(2,1,4)
        image=wall.mirror(source); hit=wall.hit(eye,image)
        self.assertEqual(hit,(0,1,2))
        self.assertAlmostEqual(a.length(a.sub(source,hit))+a.length(a.sub(hit,eye)),math.sqrt(32))
    def test_listener_right(self):
        az,el=a.arrival_angles((0,0,0),(0,0,-1),(1,0,-1))
        self.assertAlmostEqual(az,45);self.assertEqual(el,0)
    def test_tail_integral(self):
        for rt in (1.15,1.4,1.55,1.9):
            step=.0001; all_energy=late_energy=0
            for i in range(60000):
                t=(i+.5)*step
                e=((1-math.exp(-t/.025))*math.exp(-3*math.log(10)*t/rt))**2
                all_energy+=e
                if t>=.06:late_energy+=e
            self.assertAlmostEqual(late_energy/all_energy,a.tail_fraction_after(.06,rt),places=6)
            self.assertEqual(a.tail_fraction_after(-.02,rt),1)
if __name__=='__main__':unittest.main()
