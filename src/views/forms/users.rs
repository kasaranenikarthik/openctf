use wtforms::*;

#[derive(Form)]
struct LoginForm {
    #[field(name = "username")]
    username: Field<String>,
}
