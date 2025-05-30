
package body RTL is
  type t_my_type is protected body
    -- These should fail
    variable v_var1 : std_logic;
    constant c_cons1 : std_logic;
    file     f_fil1 : load_file_type open read_mode is load_file_name;
    type     t_typ1 is (idle, write, read);
    subtype  s_sub1 is integer range 0 to 9;
    alias    a_alias1 is name;

    -- These should pass
    variable v_var1 : std_logic;
    constant c_cons1 : std_logic;
    file     f_fil1 : load_file_type open read_mode is load_file_name;
    type     t_typ1 is (idle, write, read);
    subtype  s_sub1 is integer range 0 to 9;
    alias    a_alias1 is name;

    -- Test with different spacing
    variable v_var1 : std_logic;
    constant c_cons1 : std_logic;
    file     f_fil1 : load_file_type open read_mode is load_file_name;
    type     t_typ1 is (idle, write, read);
    subtype  s_sub1 is integer range 0 to 9;
    alias    a_alias1 is name;

    -- Test with shorter combinations
    constant c_sig1 : std_logic;
    file     f_fil1 : load_file_type open read_mode is load_file_name;
    type     t_typ1 is (idle, write, read);

    -- Test with comments
    variable v_var1 : std_logic;
    constant c_sig1 : std_logic;
    -- some comment
    constant c_cons1 : std_logic;
    file     f_fil1 : load_file_type open read_mode is load_file_name;
    -- some comment
    type    t_typ1 is (idle, write, read);
    subtype s_sub1 is integer range 0 to 9;

    -- Test multiline declarations
    type     state_type is (
      state1, state2,
      state3, state4
    );
    constant sig1 : std_logic;

    -- This should not error
    type state_type2 is (
      state1, state2,
      state3, state4
    );

    constant sig1 : std_logic;

    -- Checking exclusions
    constant c_abc : integer;
    function my_func return integer is
      constant c_abc : integer;
    begin
    end function;
  end protected body;

  constant c_cons1 : std_logic;
  type t_typ1 is (idle, write, read);
  subtype s_sub1 is integer range 0 to 9;

end package body RTL;

-- Test functions and procedures defined in protected body

package body RTL is
  type t_my_type is protected body
    procedure AVERAGE_SAMPLES;

    procedure AVERAGE_SAMPLES (
      constant a : in integer;
      signal b : in std_logic;
      variable c : in std_logic_vector(3 downto 0);
      signal d : out std_logic);

    function func_1 (
      constant a : integer;
      signal b : integer;
      signal c : unsigned(3 downto 0);
      signal d : std_logic_vector(7 downto 0);
      constant e : std_logic) return integer;


    -- These should fail
    variable v_var1 : std_logic;
    constant c_cons1 : std_logic;
    file     f_fil1 : load_file_type open read_mode is load_file_name;
    type     t_typ1 is (idle, write, read);
    subtype  s_sub1 is integer range 0 to 9;

  end protected body;

end package body RTL;
