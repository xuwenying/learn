      double Esci134134::esci_flwheelspeedkph(const std::uint8_t *bytes, int32_t length) const
      {
        Byte t0(bytes + 1);
        int32_t x = t0.get_byte(0, 5);

        Byte t1(bytes + 0);
        int32_t t = t1.get_byte(0, 8);
        x <<= 8;
        x |= t;

        double ret = x * 0.056250;
        return ret;
      }
