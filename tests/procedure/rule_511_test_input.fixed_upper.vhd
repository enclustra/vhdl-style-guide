package rule_511_test_input is

  procedure overflow (
    a          : integer;
    VARIABLE a : integer;
    CONSTANT a : integer;
    SIGNAL   a : integer;
    FILE     a : file_type
  );

  procedure overflow (
    a          : integer;
    VARIABLE a : integer;
    CONSTANT a : integer;
    SIGNAL   a : integer;
    FILE     a : file_type
  );

end package;

architecture rtl of test is

  procedure overflow (
    a          : integer;
    VARIABLE a : integer;
    CONSTANT a : integer;
    SIGNAL   a : integer;
    FILE     a : file_type
  ) is
  begin

  end procedure overflow;

  procedure overflow (
    a          : integer;
    VARIABLE a : integer;
    CONSTANT a : integer;
    SIGNAL   a : integer;
    FILE     a : file_type
  ) is
  begin

  end procedure overflow;

begin

end architecture rtl;
