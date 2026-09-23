const Search = (props) => {
    const {
        className='courses-search',
        type='search',
        search='',
        placeholder="Поиск курса...",
        setSearch,
    } = props
    return (<div className={`${className}`}>
              <input
                type={type}
                value={search}
                aria-label="Поиск курса"
                placeholder={placeholder}
                onChange={(event) => {setSearch(event.target.value)}}
              />
            </div>)
}

export default Search
