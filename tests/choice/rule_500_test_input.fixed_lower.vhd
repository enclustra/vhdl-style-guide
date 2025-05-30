
architecture RTL of FIFO is

begin

  -- Lower

  with a select b <=
    c when others;

  a <= (others => (others => (others => '0')));

  process (all) is
  begin

    with a select b <=
      c when others;

    a <= (others => (others => (others => '0')));

    with a select b :=
      c when others;

    a := (others => (others => (others => '0')));

    case a is
      when others =>
        null;
    end case;

  end process;

  case_gen : case a generate
    when others =>
      a <= b;
  end generate;

  -- Upper

  with a select b <=
    c when others;

  a <= (others => (others => (others => '0')));

  process (all) is
  begin

    with a select b <=
      c when others;

    a <= (others => (others => (others => '0')));

    with a select b :=
      c when others;

    a := (others => (others => (others => '0')));

    case a is
      when others =>
        null;
    end case;

  end process;

  case_gen : case a generate
    when others =>
      a <= b;
  end generate;

end architecture RTL;
