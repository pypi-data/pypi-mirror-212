JSON = ('''{{
    "{type}_{id:x}": {{
    {items}
    }}
}}''')
XML = ('''
<object type="{type}" id="{id:x}">
{items}
</object>
''')
XML_PRIMITIVE = '<primitive type="{type}">{obj}</primitive>'
XML_ITEM = ('''
<item>
    <key>
        {key}
    </key>
    <value>
        {value}
    </value>
</item>
''')