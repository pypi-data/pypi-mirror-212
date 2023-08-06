# m3u8-XZ

This is a simple package,it can download video by m3u8.

    pip install m3u8-xz

version 0.0.3 修复一些小问题

version 0.0.2 support aes-128 decode,support read local m3u8 file
    
    from m3u8_XZ import m3u8
    # use m3u8 url 通过url
    obj = m3u8(url='https://example.com/index.m3u8', folder='test')
    # use local file 通过本地文件
    # m3u8(m3u8_file='fileName.m3u8', folder='test')
    obj.run()
    

