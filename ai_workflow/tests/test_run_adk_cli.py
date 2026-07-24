from run_adk import build_parser


def test_live_parser_supports_full_flow_flag() -> None:
    args = build_parser().parse_args(["--stage", "college", "--profile", "data/profile_college_demo.txt", "--full-flow"])
    assert args.full_flow is True
