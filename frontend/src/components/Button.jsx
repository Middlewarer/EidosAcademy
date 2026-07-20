const Button = (props) => {
    const {
        children,
        className,
        type='button',
    } = props

    return (
        <button className={`login-btn ${className}`} type={type}>
            {children}
          </button>
    )
}

export default Button;